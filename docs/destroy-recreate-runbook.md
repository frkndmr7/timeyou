# TimeYou controlled destroy and recreate runbook

This runbook is specific to the current TimeYou AWS/EKS and GitOps layout. It
intentionally leaves a few recovery steps manual; it does not introduce a
secret-management service, remote Terraform backend, or additional automation.

> **Destructive operation warning:** completing the destroy permanently deletes
> ECR images, the RDS database and its managed master secret, the Cognito User
> Pool and its users, and the EKS/application workloads. The RDS final snapshot
> is intentionally disabled. Stop at every checkpoint below if the account,
> plan, resource identity, or expected diff is uncertain.

## Current ownership and important behavior

- Terraform owns the VPC, EKS, node group, RDS, Cognito, ECR repositories,
  Route 53 hosted zone, ACM certificate, Argo CD, Metrics Server, AWS Load
  Balancer Controller, and kube-prometheus-stack.
- Argo CD owns the TimeYou dev/staging/prod applications and their Ingresses.
- The production Ingress in `deploy/environments/prod/values.yaml` creates the
  internet-facing ALB. Terraform discovers that ALB by the controller stack
  tag only when `manage_production_alias = true`.
- The Route 53 hosted zone `aws_route53_zone.timeyou` is to survive teardown.
  Preserve its existing zone ID and four Namecheap-delegated name servers.
- `helm_release.argocd.create_namespace = true` is committed for fresh
  bootstrap, but is intentionally not applied to the current live release. Do
  not apply it merely to make a plan clean.
- `rds.skip_final_snapshot = true` and Cognito deletion protection is currently
  `ACTIVE`. ECR repositories do not use `force_delete`.

Commands below assume a macOS/zsh shell and the repository layout shown. Run
Terraform from `infrastructure/terraform`. Never print Terraform state, secret
values, `DATABASE_URL`, credentials, or generated passwords into logs or
terminal output.

## 1. Controlled destroy

### 1.1 Freeze and establish the exact target

1. Freeze application changes, image publishing, digest-update PRs, promotions,
   Argo syncs, and other infrastructure work. Ensure no CI run can push new ECR
   images during cleanup.
2. Confirm the expected AWS identity, region, cluster, Git state, and Kubernetes
   context. These are read-only checks:

   ```sh
   aws sts get-caller-identity --profile furkan5
   aws eks describe-cluster --profile furkan5 --region eu-west-1 \
     --name timeyou-learning --query 'cluster.{name:name,status:status,arn:arn}'
   kubectl config current-context
   kubectl get nodes -o wide
   git status --short
   git branch --show-current
   git rev-parse HEAD
   git rev-parse origin/main
   ```

   **Checkpoint:** account must be `109678733855`, region `eu-west-1`, cluster
   `timeyou-learning`, and the intended Git source must be clean and current.
   Stop if any value differs or if the cluster/context cannot be identified.

3. From `infrastructure/terraform`, record the current hosted-zone ID and
   authoritative name servers using Terraform outputs/AWS read-only queries.
   Confirm they match the zone delegated at Namecheap. Record them in the
   teardown change record; do not change the delegation.

### 1.2 Back up local Terraform state

Before any state or infrastructure mutation, securely back up the local
`terraform.tfstate` and `terraform.tfstate.backup` (if present), along with the
current Git commit and Terraform version. Use encrypted, access-controlled
storage outside the repository; do not attach the files to a commit or paste
their contents into a terminal/log. For example, after choosing a private
backup directory and confirming its permissions:

```sh
cd /Users/furkan/Projects1/timer-app/infrastructure/terraform
umask 077
cp terraform.tfstate /secure/private/location/timeyou-pre-destroy.tfstate
test ! -f terraform.tfstate.backup || \
  cp terraform.tfstate.backup /secure/private/location/timeyou-pre-destroy.tfstate.backup
```

Use the actual approved secure path in place of the example. Verify that the
backup files exist and are readable only by the authorized operator; do not
`cat`, `terraform state pull`, or otherwise dump state contents for verification.

### 1.3 Remove only the production apex alias

The first-stage setting is `manage_production_alias = false`: it suppresses
both the production ALB data lookup and the apex Alias resource. On the current
live state, switching it to false intentionally removes the existing
`timeyou.co` apex Alias; it must not be confused with a harmless default.

1. Confirm the production ALB and Ingress are still present and healthy. At
   this point the alias target must still exist while DNS is being removed.
2. Plan the gate change with the explicit false value and inspect the complete
   plan. It must show only the expected apex Alias deletion and any already
   understood, separately pending changes. In particular, the known
   `helm_release.argocd.create_namespace = false -> true` update must not be
   applied as a side effect.
3. For the teardown-only DNS mutation, use a narrowly targeted apply for the
   apex record, with the false value, after checking the targeted plan. The
   resource address may be `aws_route53_record.timeyou_apex[0]`; inspect the
   actual state address and the committed `moved` block first. Do not guess the
   address. Example shape (substitute the verified address):

   ```sh
   terraform plan -var='manage_production_alias=false' \
     -target='aws_route53_record.timeyou_apex[0]' -out=alias-teardown.tfplan
   terraform show alias-teardown.tfplan
   # Proceed only if this plan deletes only the intended apex Alias.
   terraform apply alias-teardown.tfplan
   ```

   Targeting is an exceptional teardown isolation measure here, not the normal
   Terraform workflow. If the targeted plan includes any other mutation, fails
   to address the existing record safely, or proposes the pending Argo CD
   release update, stop. Do not broaden the target or apply a full plan to
   force it through. Resolve the state-address/move condition separately before
   continuing.
4. Read-only verify the apex Alias is absent while the hosted zone, its ID, and
   its authoritative name servers remain unchanged. From here onward keep
   `manage_production_alias = false` for destroy planning so Terraform never
   looks up an ALB that is about to disappear.

### 1.4 Remove the production Ingress and wait for controller cleanup

1. Make a small GitOps change setting only production `ingress.enabled: false`
   in `deploy/environments/prod/values.yaml`. Review the diff and use the
   normal PR/check/merge process.
2. Wait for `timeyou-prod` to detect the revision, inspect its diff, and
   manually sync **only** `timeyou-prod`. Keep Argo CD and
   `aws-load-balancer-controller` running throughout this phase. Do not delete
   the Argo Application first: application removal can orphan or prune
   resources in ways that are harder to reason about than syncing the Ingress
   out of desired state.
3. Let AWS Load Balancer Controller remove the Ingress-managed ALB and related
   resources. Do not manually delete the ALB, target groups, ENIs, or generated
   security groups. Verify read-only that:

   - the `timeyou-prod` Ingress is absent;
   - the controller Deployment and pod remain Ready, with no reconciliation
     failure;
   - no ALB remains with stack tag
     `ingress.k8s.aws/stack=timeyou-prod/timeyou`;
   - no target groups remain with that stack tag;
   - no ALB-associated ENIs or controller-generated security groups for that
     stack remain.

   **Checkpoint:** do not proceed to Terraform destroy while any production
   Ingress-managed AWS resource is still deleting or remains. Allow normal
   controller cleanup time; investigate rather than manually removing an
   orphan.

### 1.5 Disable Cognito deletion protection

The User Pool currently has `deletion_protection = "ACTIVE"`. Make a temporary,
isolated Terraform configuration change to `"INACTIVE"`, then initialize,
validate, and make a full plan. The plan must be only an in-place update of
`aws_cognito_user_pool.main`, with no replacement, destroy, or other changes.
Apply this change separately and verify protection is inactive using a
read-only AWS query. Keep it inactive until the pool is destroyed. Restore
`ACTIVE` in the configuration for any future recreation.

If Terraform planning would also apply the pending Argo CD namespace
attribute, isolate this teardown-only mutation with a reviewed targeted plan
for `aws_cognito_user_pool.main`. Do not apply an unreviewed full plan merely
to disable protection. This targeted operation is not a substitute for the
normal full plan before final destroy.

### 1.6 Empty ECR repositories without changing Terraform ownership

Keep all three ECR repositories in Terraform configuration and state; the
normal destroy should delete the now-empty repositories. Do not set
`force_delete = true` and do not remove the repositories from state.

1. Confirm CI/image publishers remain frozen.
2. For each of `timeyou-frontend`, `timeyou-focus`, and `timeyou-analytics`,
   enumerate image IDs/digests read-only, then batch-delete all tagged and
   untagged image IDs through ECR. Paginate the list and respect the API's
   batch-size limit. Do not delete a repository at this stage.
3. Verify each repository has zero images. If new images appear or deletion
   errors leave images behind, stop and repeat the inventory safely before
   Terraform destroy.

This intentionally loses the immutable artifacts. The recreate process builds
and publishes new images through CI.

### 1.7 Final pre-destroy checks and preserve the hosted zone

1. Confirm prod Ingress/ALB cleanup is complete, the apex Alias is absent,
   Cognito deletion protection is inactive, ECR repositories are empty, and
   there are no active changes or CI publishers.
2. Take a second secure backup of the current Terraform state and backup file.
   Keep the pre-destroy backup too.
3. Remove only the hosted zone from Terraform state, preserving the AWS zone:

   ```sh
   cd /Users/furkan/Projects1/timer-app/infrastructure/terraform
   terraform state rm aws_route53_zone.timeyou
   ```

   This is an intentional ownership handoff for teardown. It does not delete
   the AWS hosted zone. Do not remove the ACM validation record separately
   unless the reviewed destroy plan shows it is required; Terraform should
   remove its managed record while retaining the zone.
4. **After `terraform state rm`, do not run a normal `terraform plan` or
   `terraform apply`.** The configuration still declares the zone, so an
   ordinary plan may propose creating a replacement hosted zone. Proceed
   directly to the destroy-only plan below. If that plan is not immediately
   ready, stop and carefully restore/reconcile state rather than running a
   normal apply.
5. Run the full destroy plan with the alias gate false and inspect it:

   ```sh
   terraform plan -destroy -var='manage_production_alias=false' \
     -out=final-destroy.tfplan
   terraform show final-destroy.tfplan
   ```

   **GO checkpoint:** the retained hosted zone must not appear as a deletion
   or creation; production ALB lookup must not be required; no unexpected
   resource replacement or unrelated target may appear. Confirm the plan
   includes only the intended remaining managed infrastructure. The pending
   `create_namespace` change must not be applied: it is configuration drift in
   an existing release, not a prerequisite to destroying it.

### 1.8 Run Terraform destroy and inspect leftovers

Only after the preceding plan passes the GO checkpoint:

```sh
terraform destroy -var='manage_production_alias=false'
```

Review Terraform's final confirmation prompt against the approved plan. Do not
approve if the target account, region, hosted zone, resource list, or operation
has changed since review. Keep the hosted zone and Namecheap delegation intact.

After destroy:

- Verify Terraform reports completion; investigate any partial failure before
  retrying. Never overwrite an updated state with the pre-destroy backup to
  make a partial destroy appear complete.
- Securely back up the resulting final Terraform state as an audit record.
- Read-only check for billable or controller-created orphans: ALBs, target
  groups, ENIs, security groups, Elastic IPs/NAT Gateways, EBS volumes,
  snapshots, RDS instances/secrets, ECR repositories, and unexpected running
  EC2 instances. The hosted zone is the planned survivor.
- Verify the retained hosted-zone ID and four name servers still match the
  recorded/delegated values. Do not change Namecheap.

## 2. Recreate

### 2.1 Prepare repository, Terraform workspace, and retained DNS zone

1. Check out the intended clean `main` revision and verify it before running
   Terraform. Use the repository's current provider lock file and Terraform
   version constraints.
2. Prepare `infrastructure/terraform` and initialize the local backend. Do not
   copy a stale pre-destroy state into the new workspace. Keep all state and
   plan files out of Git and in private storage.
3. Prepare a real, untracked `terraform.tfvars` from
   `terraform.tfvars.example`. Fill required account/network/Cognito-prefix/
   access inputs from the operator's current decisions; do not place secrets
   in the example file. Use the current intended public API CIDR allowlist.
4. Import the retained Route 53 hosted zone before applying the platform:

   ```sh
   terraform import aws_route53_zone.timeyou <PRESERVED_HOSTED_ZONE_ID>
   terraform plan -var='manage_production_alias=false'
   ```

   **Checkpoint:** the import must refer to the recorded existing zone ID and
   the plan must preserve that zone and its existing name servers. If Terraform
   proposes replacement or deletion, stop. Do not apply until the imported
   zone is represented without an unintended change.
5. Set `manage_production_alias = false` for first-stage bootstrap. Never use
   the example file unchanged without reviewing its other inputs.

### 2.2 Bootstrap AWS and platform services

1. Run `terraform fmt -check` and `terraform validate`.
2. Review the full first-stage plan with the alias gate false. It must not query
   for or create the production ALB alias. Review all account/region/resource
   identities before applying.
3. Apply the approved infrastructure plan. The dependency graph installs
   Argo CD and Terraform-owned platform add-ons after the EKS node group is
   ready. Wait for EKS nodes and platform Helm releases to become healthy.
4. Configure Kubernetes access and verify the intended context, nodes, Argo CD,
   AWS Load Balancer Controller, Metrics Server, and monitoring stack.

### 2.3 Restore the documented manual prerequisites

Complete these manual steps without putting secret values in Git:

- Restore Argo's GitHub App repository credential as Secret
  `argocd/timeyou-repo`; use the approved GitHub App installation and private
  key. Confirm Argo can read `frkndmr7/timeyou` before creating/syncing its
  applications.
- Create `timeyou-runtime` in `timeyou-dev`, `timeyou-staging`, and
  `timeyou-prod`, with `DATABASE_URL` and `FOCUS_INTERNAL_API_KEY`. Supply
  environment-correct values through the approved secure operator process;
  never commit or print them.
- Create the `timeyou_staging` and `timeyou_prod` databases manually in the
  recreated private PostgreSQL instance and ensure the application DB user
  has the required privileges. Confirm authoritative RDS-managed credentials
  and the runtime Secret agree before starting Focus workloads.
- Recreate any environment-specific non-secret/manual bootstrap settings that
  are not Terraform-owned, following the current application configuration.

### 2.4 Restore application delivery and environment identifiers

1. CI must build and publish the frontend, Focus, and Analytics images to the
   recreated ECR repositories. Use the normal immutable-digest dev update PR;
   then promote the same verified digests dev → staging → prod through the
   existing PR process. Do not hand-edit digests to guessed tags.
2. Recreate Cognito through Terraform. Its User Pool ID, App Client ID,
   Managed Login domain/prefix, and issuer will be new. Update the relevant
   environment values with the new non-secret identifiers and callback/logout
   allowlists. Keep localhost URLs only if still required and explicitly
   allowlisted. Validate rendered runtime config before application sync.
3. Recreate the ACM certificate through Terraform. After it is issued, copy
   the new certificate ARN into the production Ingress annotation in
   `deploy/environments/prod/values.yaml` and merge that reviewed GitOps
   change. The old ARN is not reusable.
4. Apply the Argo Application manifests from `deploy/argocd` using the
   documented bootstrap process, after `timeyou-repo` credentials are
   available. Manually sync dev first, then staging and prod in order. Verify
   each environment's workloads and database migrations before proceeding to
   the next.
5. Keep the production Ingress disabled or otherwise absent until its image,
   runtime Secret, database, Cognito values, and ACM certificate are ready.
   Enable/sync the production Ingress and wait for the controller-created ALB
   to become active with healthy target groups and HTTPS listener.

### 2.5 Re-enable apex DNS in the second stage

Only after the production Ingress has created a healthy ALB:

1. Change `manage_production_alias` to `true` in the reviewed local Terraform
   input/configuration used for this environment.
2. Run a normal Terraform plan. Confirm it discovers the intended production
   ALB by the `timeyou-prod/timeyou` stack tag and proposes only the intended
   apex Alias creation (plus no unexpected infrastructure changes).
3. Apply the reviewed plan and verify `timeyou.co` resolves to the ALB, HTTPS
   uses the new valid certificate, HTTP redirects to HTTPS, and frontend,
   Focus health, and expected Analytics authentication behavior work publicly.

## Expected intentional data loss

- All three ECR repositories and their images are deleted; images are rebuilt
  during recreate.
- The RDS instance, application data, and RDS-managed master credential are
  deleted without a final snapshot. Staging/prod databases are bootstrapped
  again manually.
- The Cognito User Pool and all users are deleted. Users must register again;
  recreated Cognito identifiers must be propagated to environment config.
- EKS workloads, Argo CD runtime configuration, and Kubernetes Secrets are
  deleted and recreated as part of the platform/application bootstrap.

## What survives destroy

- The Route 53 public hosted zone, its zone ID, and its four authoritative name
  servers remain in AWS and continue to be delegated from Namecheap.
- The Namecheap domain registration and nameserver delegation remain unchanged.
- Secure local Terraform state backups and the final post-destroy state record
  remain under operator control.

## What must be recreated manually

- Argo GitHub App repository credential `argocd/timeyou-repo`.
- `timeyou-runtime` Secrets for dev/staging/prod, including
  `DATABASE_URL` and `FOCUS_INTERNAL_API_KEY`.
- `timeyou_staging` and `timeyou_prod` databases and any required grants.
- GitHub Actions external settings if required by the new repository/ECR
  resources.
- Environment values for recreated Cognito identifiers and the new ACM
  certificate ARN, through reviewed Git changes.
