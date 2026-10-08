resource "aws_iam_instance_profile" "ssm_profile" {
  name = "test-ec2-ssm-profile"
  role = aws_iam_role.ec2_role.name
}

