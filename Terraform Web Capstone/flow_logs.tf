resource "aws_flow_log" "terraform_capstone_flow_log" {
  iam_role_arn    = aws_iam_role.terraform_capstone_flow_log_role.arn
  log_destination = aws_cloudwatch_log_group.terraform_capstone_flow_log_group.arn
  traffic_type    = "ALL"
  vpc_id          = aws_vpc.Terraform_Web_Vpc.id
}

