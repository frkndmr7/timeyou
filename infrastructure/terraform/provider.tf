provider "aws" {
  region              = var.aws_region
  allowed_account_ids = [var.allowed_aws_account_id]
}
