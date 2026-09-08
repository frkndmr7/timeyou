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
