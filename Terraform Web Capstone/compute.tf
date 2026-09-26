resource "aws_network_interface" "terraform_capstone_network_interface" {
  subnet_id       = aws_subnet.Terraform_Web_Subnet_A.id
  private_ips     = ["10.0.1.10"]
  security_groups = [aws_security_group.Security_Rules.id]

  tags = {
    Name = "primary_network_interface"
  }
}

# resource "aws_instance" "test" {
#   ami           = "ami-0d7f022123f8ff19d"
#   instance_type = "t3.micro"

#   iam_instance_profile = aws_iam_instance_profile.ec2_profile.name

#   user_data = <<-EOF
#               #!/bin/bash
#               yes | sudo apt update
#               yes | sudo apt install apache2
#               echo "<h1>Server Details</h1><p><strong>Hostname:</strong> \$(hostname)</p><p><strong>IP Address:</strong> \$(hostname -I | cut -d' ' -f1)</p>" > /var/www/html/index.html
#               sudo systemctl restart apache2
#               EOF

#   primary_network_interface {
#     network_interface_id = aws_network_interface.example.id
#   }

#   credit_specification {
#     cpu_credits = "unlimited"
#   }
# }