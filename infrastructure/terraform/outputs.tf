output "frontend_repository_url" {
  description = "ECR URL for the Time&You frontend image."
  value       = aws_ecr_repository.frontend.repository_url
}

output "focus_repository_url" {
  description = "ECR URL for the Time&You Focus Service image."
  value       = aws_ecr_repository.focus.repository_url
}

output "analytics_repository_url" {
  description = "ECR URL for the Time&You Analytics Service image."
  value       = aws_ecr_repository.analytics.repository_url
}

output "frontend_repository_arn" {
  description = "ECR ARN for the Time&You frontend image."
  value       = aws_ecr_repository.frontend.arn
}

output "focus_repository_arn" {
  description = "ECR ARN for the Time&You Focus Service image."
  value       = aws_ecr_repository.focus.arn
}

output "analytics_repository_arn" {
  description = "ECR ARN for the Time&You Analytics Service image."
  value       = aws_ecr_repository.analytics.arn
}

output "vpc_id" {
  description = "ID of the Time&You learning VPC."
  value       = aws_vpc.main.id
}

output "eks_cluster_name" {
  description = "Name of the Time&You learning EKS cluster."
  value       = aws_eks_cluster.main.name
}

output "eks_cluster_endpoint" {
  description = "Kubernetes API endpoint for the Time&You learning EKS cluster."
  value       = aws_eks_cluster.main.endpoint
}

output "eks_node_group_name" {
  description = "Name of the Time&You learning EKS managed node group."
  value       = aws_eks_node_group.main.node_group_name
}

output "postgres_endpoint" {
  description = "Endpoint hostname for the private PostgreSQL RDS instance."
  value       = aws_db_instance.postgres.address
}

output "postgres_port" {
  description = "Port for the private PostgreSQL RDS instance."
  value       = aws_db_instance.postgres.port
}

output "postgres_database_name" {
  description = "Initial database name for the PostgreSQL RDS instance."
  value       = aws_db_instance.postgres.db_name
}

output "postgres_master_user_secret_arn" {
  description = "AWS Secrets Manager ARN managed by RDS for the PostgreSQL master credentials."
  value       = aws_db_instance.postgres.master_user_secret[0].secret_arn
}

output "github_actions_ecr_role_arn" {
  description = "IAM role ARN for the source repository GitHub Actions ECR push workflow."
  value       = aws_iam_role.github_actions_ecr.arn
}

output "aws_load_balancer_controller_role_arn" {
  description = "IRSA role ARN for the AWS Load Balancer Controller service account."
  value       = aws_iam_role.aws_load_balancer_controller.arn
}

output "cognito_user_pool_id" {
  description = "ID of the Time&You Cognito User Pool."
  value       = aws_cognito_user_pool.main.id
}

output "cognito_issuer_url" {
  description = "JWT issuer URL for the Time&You Cognito User Pool."
  value       = "https://cognito-idp.${var.aws_region}.amazonaws.com/${aws_cognito_user_pool.main.id}"
}

output "cognito_app_client_id" {
  description = "Public OAuth app client ID for Time&You."
  value       = aws_cognito_user_pool_client.timeyou.id
}

output "cognito_managed_login_url" {
  description = "Base URL for the Cognito managed login domain."
  value       = "https://${aws_cognito_user_pool_domain.main.domain}.auth.${var.aws_region}.amazoncognito.com"
}
