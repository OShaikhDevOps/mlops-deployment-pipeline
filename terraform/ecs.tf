/*
Minimal ECS/Fargate stack using the default VPC. This creates an ECS cluster, task definition that
pulls the image from ECR, and a Fargate service attached to an ALB.
Customize task role, execution role, and networking for production use.
*/

data "aws_vpc" "default" {
	default = true
}

data "aws_subnet_ids" "default" {
	vpc_id = data.aws_vpc.default.id
}

resource "aws_security_group" "alb_sg" {
	name   = "${var.project_name}-alb-sg"
	vpc_id = data.aws_vpc.default.id

	ingress {
		from_port   = 80
		to_port     = 80
		protocol    = "tcp"
		cidr_blocks = ["0.0.0.0/0"]
	}

	egress {
		from_port   = 0
		to_port     = 0
		protocol    = "-1"
		cidr_blocks = ["0.0.0.0/0"]
	}
}

resource "aws_lb" "alb" {
	name               = "${var.project_name}-alb"
	internal           = false
	load_balancer_type = "application"
	security_groups    = [aws_security_group.alb_sg.id]
	subnets            = data.aws_subnet_ids.default.ids
}

resource "aws_lb_target_group" "tg" {
	name     = "${var.project_name}-tg"
	port     = 80
	protocol = "HTTP"
	vpc_id   = data.aws_vpc.default.id
	health_check {
		path                = "/health"
		interval            = 30
		timeout             = 5
		healthy_threshold   = 2
		unhealthy_threshold = 2
	}
}

resource "aws_lb_listener" "http" {
	load_balancer_arn = aws_lb.alb.arn
	port              = "80"
	protocol          = "HTTP"

	default_action {
		type             = "forward"
		target_group_arn = aws_lb_target_group.tg.arn
	}
}

resource "aws_ecs_task_definition" "app" {
	family                   = "${var.project_name}-task"
	requires_compatibilities = ["FARGATE"]
	cpu                      = "256"
	memory                   = "512"
	network_mode             = "awsvpc"
	execution_role_arn       = aws_iam_role.ecs_task_execution.arn

	container_definitions = jsonencode([
		{
			name      = "app",
			image     = "${aws_ecr_repository.app.repository_url}:latest",
			essential = true,
			portMappings = [ { containerPort = 80 } ],
			environment = [ { name = "MLFLOW_TRACKING_URI", value = "s3://${aws_s3_bucket.mlops_artifacts.bucket}" } ]
		}
	])
}

resource "aws_ecs_service" "app_service" {
	name            = "${var.project_name}-service"
	cluster         = aws_ecs_cluster.mlops_cluster.id
	task_definition = aws_ecs_task_definition.app.arn
	launch_type     = "FARGATE"
	desired_count   = 1

	network_configuration {
		subnets         = data.aws_subnet_ids.default.ids
		security_groups = [aws_security_group.alb_sg.id]
		assign_public_ip = true
	}

	load_balancer {
		target_group_arn = aws_lb_target_group.tg.arn
		container_name   = "app"
		container_port   = 80
	}
}
