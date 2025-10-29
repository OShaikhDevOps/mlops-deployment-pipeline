output "ecr_repo_url" {
  value = aws_ecr_repository.app.repository_url
}

output "s3_artifacts_bucket" {
  value = aws_s3_bucket.mlops_artifacts.id
}

output "ecs_cluster_name" {
  value = aws_ecs_cluster.this.name
}
