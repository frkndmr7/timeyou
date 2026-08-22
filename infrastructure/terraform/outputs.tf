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
