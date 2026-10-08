
# ============================================================
# VPC
# ============================================================

resource "aws_vpc" "Terraform_Web_Vpc" {
  cidr_block = "10.0.0.0/16"

    tags = {
    Name = "Terraform Web VPC"
  }
}

# ============================================================
# Private Subnet 1 (us-east-1a)
# ============================================================

resource "aws_subnet" "Terraform_Web_Subnet_A" {
  vpc_id            = aws_vpc.Terraform_Web_Vpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-east-1a"
  #map_public_ip_on_launch = "true"

  tags = {
    Name = "Subnet A"
  }
}
# ============================================================
# Private Subnet 2 (us-east-1b)
# ============================================================

resource "aws_subnet" "Terraform_Web_Subnet_B" {
  vpc_id            = aws_vpc.Terraform_Web_Vpc.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "us-east-1b"
  #map_public_ip_on_launch = "true"

  tags = {
    Name = "Subnet B"
  }
}


# ============================================================
# ALB Public Subnet
# ============================================================
resource "aws_subnet" "ALB-Subnet" {
  vpc_id                  = aws_vpc.Terraform_Web_Vpc.id
  cidr_block              = "10.0.3.0/24"
  map_public_ip_on_launch = "true"
  availability_zone       = "us-east-1a"

  tags = {
    Name = "ALB SUBNET"
  }
}

# ============================================================
# ALB Public Subnet B
# ============================================================
resource "aws_subnet" "ALB-Subnet-B" {
  vpc_id                  = aws_vpc.Terraform_Web_Vpc.id
  cidr_block              = "10.0.5.0/24"
  map_public_ip_on_launch = "true"
  availability_zone       = "us-east-1b"

  tags = {
    Name = "ALB subnet B"
  }
}

# ============================================================
# NAT Public Subnet
# ============================================================
resource "aws_subnet" "NAT-Subnet" {
  vpc_id                  = aws_vpc.Terraform_Web_Vpc.id
  cidr_block              = "10.0.4.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = "true"

  tags = {
    Name = "NAT subnet"
  }
}
#IGW  

resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.Terraform_Web_Vpc.id

  tags = {
    Name = "main"
  }
}


# ============================================================
# Route Table for Subnet A & B
# ============================================================

resource "aws_route_table" "RT" {
  vpc_id = aws_vpc.Terraform_Web_Vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat_a.id
  }


  tags = {
    Name = "Route Table Subnet A & B"
  }
}


# ============================================================
# Route Table for NAT
# ============================================================

resource "aws_route_table" "RT-NAT" {
  vpc_id = aws_vpc.Terraform_Web_Vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id

  }


  tags = {
    Name = "Route Table NAT"
  }
}



# ============================================================
# ALB ROUTE TABLE
# ============================================================

resource "aws_route_table" "ALB-RT" {
  vpc_id = aws_vpc.Terraform_Web_Vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id

  }


  tags = {
    Name = "ALB RT"
  }
}

# ============================================================
# Route Table Assosiation(s)
# ============================================================


# ============================================================
# Subnet A
# ============================================================

resource "aws_route_table_association" "rt_assosiation" {
  subnet_id      = aws_subnet.Terraform_Web_Subnet_A.id
  route_table_id = aws_route_table.RT.id
}




# ============================================================
# Subnet B
# ============================================================

resource "aws_route_table_association" "rt_assosiation_b" {
  subnet_id      = aws_subnet.Terraform_Web_Subnet_B.id
  route_table_id = aws_route_table.RT.id
}

# ============================================================
# ALB subnet
# ============================================================

resource "aws_route_table_association" "rt_assosiation_alb" {
  subnet_id      = aws_subnet.ALB-Subnet.id
  route_table_id = aws_route_table.ALB-RT.id
}

# ============================================================
# Second ALB subnet
# ============================================================

resource "aws_route_table_association" "rt_assosiation_alb_b" {
  subnet_id      = aws_subnet.ALB-Subnet-B.id
  route_table_id = aws_route_table.ALB-RT.id
}

# ============================================================
# NAT subnet
# ============================================================

resource "aws_route_table_association" "rt_assosiation_nat" {
  subnet_id      = aws_subnet.NAT-Subnet.id
  route_table_id = aws_route_table.RT-NAT.id
}


# ============================================================
# NAT Configuration
# ============================================================

resource "aws_eip" "nat_a" {
  domain = "vpc"

  tags = {
    Name = "NAT-A-EIP"
  }
}

resource "aws_nat_gateway" "nat_a" {
  allocation_id = aws_eip.nat_a.id
  subnet_id     = aws_subnet.NAT-Subnet.id

  tags = {
    Name = "gw NAT A"
  }

  depends_on = [aws_internet_gateway.gw]
}

#Wait for NAT
resource "time_sleep" "wait_for_nat" {
  depends_on      = [aws_nat_gateway.nat_a, aws_route_table.RT]
  create_duration = "60s"
}
