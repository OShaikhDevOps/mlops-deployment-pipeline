# Terraform skeleton

This folder contains Terraform files that provide a starting point for deploying the app to AWS.

Files:
- `provider.tf` - provider and required providers
- `variables.tf` - variables used by the config
- `random.tf` - random name suffix resource
- `main.tf` - S3 bucket and ECS cluster resources
- `ecr.tf` - example ECR repository resource
- `ecs.tf` - ECS task/service/ALB skeleton (uses default VPC)
- `iam.tf` - IAM roles for ECS task execution

Before applying:
- Review and set variables where required.
- Ensure the AWS principal you use has permission to create S3, ECS, ECR, IAM and ALB resources.
- Terraform will create real cloud resources - expect charges.

Example:

```powershell
cd terraform
terraform init
terraform plan -out=tfplan
terraform apply -auto-approve
```
