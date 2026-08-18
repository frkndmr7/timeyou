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
