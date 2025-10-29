terraform {
  required_version = ">= 1.0"
}

provider "aws" {
  region = var.aws_region
}

locals {
  bucket_name = length(var.s3_bucket_name) > 0 ? var.s3_bucket_name : "${var.project_name}-artifacts-${random_pet.name_suffix.id}"
}

resource "aws_s3_bucket" "mlops_artifacts" {
  bucket = local.bucket_name

  tags = {
    Name = "${var.project_name}-artifacts"
  }
}

resource "aws_s3_bucket_public_access_block" "block" {
  bucket = aws_s3_bucket.mlops_artifacts.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_ecs_cluster" "mlops_cluster" {
  name = "${var.project_name}-cluster"
}

output "s3_bucket" {
  value = aws_s3_bucket.mlops_artifacts.bucket
}

output "ecs_cluster" {
  value = aws_ecs_cluster.mlops_cluster.name
}
