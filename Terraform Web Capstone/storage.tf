# ============================================================
# S3 Buckets
# ============================================================


resource "aws_s3_bucket" "terraform-capstone-s3" {
  bucket = "terraform-capstone-s3"

  tags = {
    Name        = "Terraform_Capstone_S3"
    Environment = "Dev"
  }
}

# ============================================================
# Block Public Access
# ============================================================

resource "aws_s3_bucket_public_access_block" "example" {
  bucket = aws_s3_bucket.terraform-capstone-s3.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# ============================================================
# ALB Logs
# ============================================================

resource "aws_s3_bucket" "terraform-capstone-s3-alb-logs" {
  bucket = "terraform-capstone-s3-alb-logs"

  tags = {
    Name        = "Terraform_Capstone_S3-ALB"
    Environment = "Dev"
  }
}
