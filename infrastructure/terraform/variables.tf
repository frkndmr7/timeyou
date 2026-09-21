variable "aws_region" {
  description = "AWS region for the Time&You resources."
  type        = string
  default     = "eu-west-1"
}

variable "allowed_aws_account_id" {
  description = "Explicit AWS account ID allowed for Terraform operations in this working copy."
  type        = string
  nullable    = false

  validation {
    condition     = can(regex("^[0-9]{12}$", var.allowed_aws_account_id))
    error_message = "allowed_aws_account_id must be a 12-digit AWS account ID."
  }
}

variable "vpc_cidr" {
  description = "CIDR block for the learning VPC."
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "Two availability zones used by the learning VPC."
  type        = list(string)
  default     = ["eu-west-1a", "eu-west-1b"]

  validation {
    condition     = length(var.availability_zones) == 2
    error_message = "Exactly two availability zones must be configured."
  }
}

variable "cluster_name" {
  description = "Name of the learning EKS cluster."
  type        = string
  default     = "timeyou-learning"
}

variable "eks_version" {
  description = "Kubernetes version for the EKS control plane and managed node group."
  type        = string
  default     = "1.36"
}

variable "cluster_public_access_cidrs" {
  description = "CIDR blocks allowed to reach the public EKS API endpoint. Use the operator's public IP as an /32."
  type        = list(string)

  validation {
    condition     = length(var.cluster_public_access_cidrs) > 0
    error_message = "At least one public EKS API endpoint CIDR must be provided."
  }
}

variable "manage_production_alias" {
  description = "Whether Terraform should discover the production ALB and manage the timeyou.co apex alias. Disable during fresh platform bootstrap until the Argo-managed Ingress has created the ALB."
  type        = bool
  default     = true
}

variable "database_name" {
  description = "Initial PostgreSQL database name for Focus Service."
  type        = string
  default     = "timeyou"
}

variable "database_username" {
  description = "Managed PostgreSQL master username for the learning environment."
  type        = string
  default     = "timeyou_app"
}

variable "github_repository" {
  description = "GitHub source repository allowed to assume the ECR push role."
  type        = string
  default     = "frkndmr7/timeyou"
}

variable "github_branch" {
  description = "GitHub branch allowed to assume the ECR push role."
  type        = string
  default     = "main"
}

variable "cognito_user_pool_name" {
  description = "Name for the Time&You Cognito User Pool."
  type        = string
  default     = "timeyou"
}

variable "cognito_domain_prefix" {
  description = "Unique Cognito managed login domain prefix for this AWS account and region."
  type        = string
  nullable    = false

  validation {
    condition     = can(regex("^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$", var.cognito_domain_prefix))
    error_message = "cognito_domain_prefix must be 1-63 lowercase letters, numbers, or hyphens and cannot start or end with a hyphen."
  }
}

variable "cognito_callback_urls" {
  description = "Allowed OAuth callback URLs for the public Cognito app client."
  type        = list(string)
  default = [
    "http://localhost:3001/auth/callback",
    "https://timeyou.co/auth/callback",
  ]
}

variable "cognito_logout_urls" {
  description = "Allowed logout URLs for the public Cognito app client."
  type        = list(string)
  default = [
    "http://localhost:3001",
    "https://timeyou.co",
  ]
}
