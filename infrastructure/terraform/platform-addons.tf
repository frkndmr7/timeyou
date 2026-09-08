resource "helm_release" "metrics_server" {
  name             = "metrics-server"
  namespace        = "kube-system"
  repository       = "https://kubernetes-sigs.github.io/metrics-server/"
  chart            = "metrics-server"
  version          = "3.14.0"
  create_namespace = false
  wait             = true
  recreate_pods    = false
  force_update     = false
  upgrade_install  = true
  take_ownership   = true

  values = [yamlencode({
    replicas = 1
  })]
}

resource "helm_release" "aws_load_balancer_controller" {
  name             = "aws-load-balancer-controller"
  namespace        = "kube-system"
  repository       = "https://aws.github.io/eks-charts"
  chart            = "aws-load-balancer-controller"
  version          = "3.5.0"
  create_namespace = false
  wait             = true
  recreate_pods    = false
  force_update     = false
  upgrade_install  = true
  take_ownership   = true
  skip_crds        = false

  values = [yamlencode({
    clusterName  = "timeyou-learning"
    region       = "eu-west-1"
    vpcId        = "vpc-0cf60a919e5ffbaa3"
    replicaCount = 1
    serviceAccount = {
      create = true
      name   = "aws-load-balancer-controller"
      annotations = {
        "eks.amazonaws.com/role-arn" = "arn:aws:iam::109678733855:role/timeyou-learning-aws-load-balancer-controller"
      }
    }
  })]
}
