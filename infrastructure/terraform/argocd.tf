data "aws_eks_cluster_auth" "main" {
  name = aws_eks_cluster.main.name
}

resource "helm_release" "argocd" {
  name             = "argocd"
  namespace        = "argocd"
  repository       = "https://argoproj.github.io/argo-helm"
  chart            = "argo-cd"
  version          = "10.4.2"
  create_namespace = true

  depends_on = [aws_eks_node_group.main]

  values = [yamlencode({
    dex = {
      enabled = false
    }
    notifications = {
      enabled = false
    }
    "redis-ha" = {
      enabled = false
    }
    server = {
      service = {
        type = "ClusterIP"
      }
    }
  })]
}
