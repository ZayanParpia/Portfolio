#ALB

resource "aws_lb" "Terraform_ALB" {
  name               = "test-lb-tf"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.Security_Rules.id]
  subnets            = [aws_subnet.ALB-Subnet.id, aws_subnet.ALB-Subnet-B.id]

  enable_deletion_protection = false


  #Will Add this later

  #access_logs {
  #bucket  = aws_s3_bucket.terraform-capstone-s3-alb-logs.id
  #prefix  = "test-lb"
  #enabled = true
  #}

  tags = {
    Environment = "Development"
  }
}

#TARGET GROUP
resource "aws_lb_target_group" "target_group" {
  name        = "terraform-capstone-tg"
  port        = 80
  protocol    = "HTTP"
  target_type = "instance"
  vpc_id      = aws_vpc.Terraform_Web_Vpc.id

  health_check {
    enabled             = true
    path                = "/"
    protocol            = "HTTP"
    port                = "traffic-port"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 3
    unhealthy_threshold = 3
    matcher             = "200"
  }
}

#LISTENER

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.Terraform_ALB.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.target_group.arn
  }
}