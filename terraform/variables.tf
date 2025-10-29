variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "project_name" {
  type    = string
  default = "mlops-demo"
}

variable "ecr_repo_name" {
  type    = string
  default = "mlops-demo-repo"
}

variable "s3_bucket_name" {
  type    = string
  default = ""
  description = "If empty, Terraform will create a bucket with project name and a random suffix."
}
