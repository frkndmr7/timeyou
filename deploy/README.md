# Time&You GitOps

This repository contains the Kubernetes desired state for Time&You environments.

## Promotion Flow

The promotion model is based on one immutable artifact:

> **Promote the verified artifact; do not rebuild it.**

1. CI builds the frontend, focus, and analytics images once for a source commit.
2. CI pushes the images to ECR using the immutable Git SHA tag.
3. CI updates only the image digests in `environments/dev/values.yaml` through a GitOps pull request.
4. Dev is deployed and verified.
5. Staging promotion does not rebuild any image.
6. The verified frontend, focus, and analytics `repository@digest` values are copied unchanged from `environments/dev/values.yaml` to `environments/staging/values.yaml`.
7. The staging digest change is reviewed and merged as a separate, controlled GitOps pull request.
8. After merge, staging is deployed with a manual Argo CD sync.
9. Staging smoke and end-to-end tests are run.

Environment-specific configuration is supplied at runtime, not baked into the image:

- Public frontend configuration is provided through Helm/ConfigMap runtime wiring.
- Private runtime configuration is provided through the namespace-local `timeyou-runtime` Secret.

CI does not modify staging automatically. A promotion pull request should contain only the required staging digest changes. Environment-specific values and secrets must not be copied blindly from dev to staging.
