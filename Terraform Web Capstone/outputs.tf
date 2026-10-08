# ============================================================
# ALB DNS NAME
# ============================================================


output "alb_dns_name" {
  description = "DNS name of the Application Load Balancer"
  value       = aws_lb.Terraform_ALB.dns_name
}

# output "ec2-private_ip" {
#   description = "Private IP address of the EC2 instance"
#   value       = aws_instance.Terraform_EC2.private_ip
# }