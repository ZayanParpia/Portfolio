#Launch Table

resource "aws_launch_template" "Autoscale-LaunchTemplate" {
  name_prefix            = "foobar"
  image_id               = "ami-0d7f022123f8ff19d"
  instance_type          = "t3.micro"
  vpc_security_group_ids = [aws_security_group.Security_Rules.id]

  iam_instance_profile {
    name = aws_iam_instance_profile.ec2_profile.name
  }

  user_data = base64encode(<<-EOF
              #!/bin/bash
              yes | sudo wget https://s3.amazonaws.com/mountpoint-s3-release/latest/x86_64/mount-s3.deb
              yes | sudo apt update
              yes | sudo apt install apache2
              yes | sudo apt-get install -y ./mount-s3.deb
              sudo mkdir -p /mnt/s3
              sudo chown $(whoami):$(whoami) /mnt/s3
              mount-s3 terraform-capstone-s3 /mnt/s3
              echo "<h1>Server Details</h1><p><strong>Hostname:</strong> $(hostname)</p><p><strong>IP Address:</strong> $(hostname -I | cut -d' ' -f1)</p>" > /var/www/html/index.html
              sudo systemctl restart apache2
              EOF
  )
}

resource "aws_autoscaling_group" "asg" {
  desired_capacity    = 1
  max_size            = 3
  min_size            = 1
  vpc_zone_identifier = [aws_subnet.Terraform_Web_Subnet_A.id, aws_subnet.Terraform_Web_Subnet_B.id]
  depends_on          = [time_sleep.wait_for_nat]

  target_group_arns = [aws_lb_target_group.target_group.arn]

  launch_template {
    id      = aws_launch_template.Autoscale-LaunchTemplate.id
    version = "$Latest"
  }
}


resource "aws_autoscaling_policy" "autoscale-policy" {
  name                   = "autoscale-policy"
  autoscaling_group_name = aws_autoscaling_group.asg.name
  policy_type            = "TargetTrackingScaling"

  target_tracking_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ASGAverageCPUUtilization"
    }
    target_value = 10 #Change Later
  }
}
