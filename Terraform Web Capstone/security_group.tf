# ============================================================
# Security Group
# ============================================================


resource "aws_security_group" "Security_Rules" {
  name        = "Security Rules Terraform Capstone"
  description = "Security Rules"
  vpc_id      = aws_vpc.Terraform_Web_Vpc.id

  tags = {
    Name = "Security Rules"
  }
}

# ============================================================
# Allow port 80 and 443 for ALB
# ============================================================

resource "aws_vpc_security_group_ingress_rule" "allow_http_ipv4" {
  security_group_id = aws_security_group.Security_Rules.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 80
  ip_protocol       = "tcp"
  to_port           = 80
}

resource "aws_vpc_security_group_ingress_rule" "allow_https_ipv4" {
  security_group_id = aws_security_group.Security_Rules.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 443
  ip_protocol       = "tcp"
  to_port           = 443
}


resource "aws_vpc_security_group_egress_rule" "allow_all_traffic_ipv4" {
  security_group_id = aws_security_group.Security_Rules.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1" # semantically equivalent to all ports
}

