variable "aws_region" {
  description = "AWS region for the Time&You resources."
  type        = string
  default     = "eu-central-1"
}

variable "vpc_cidr" {
  description = "CIDR block for the learning VPC."
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "Two availability zones used by the learning VPC."
  type        = list(string)
  default     = ["eu-central-1a", "eu-central-1b"]

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
  default     = "1.34"
}

variable "cluster_public_access_cidrs" {
  description = "CIDR blocks allowed to reach the public EKS API endpoint. Use the operator's public IP as an /32."
  type        = list(string)

  validation {
    condition     = length(var.cluster_public_access_cidrs) > 0
    error_message = "At least one public EKS API endpoint CIDR must be provided."
  }
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
