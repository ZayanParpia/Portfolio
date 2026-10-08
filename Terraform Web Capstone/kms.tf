resource "aws_kms_key" "terraform_capstone_s3_key" {
  description             = "KMS key for S3 bucket encryption"
  deletion_window_in_days = 10
  enable_key_rotation     = true

  tags = {
    Name        = "Terraform_Capstone_S3_KMS_KEY"
    Environment = "Dev"
  }
}

resource "aws_kms_alias" "my_key_alias" {
  name          = "alias/terraform_capstone_s3_key"
  target_key_id = aws_kms_key.terraform_capstone_s3_key.key_id
}

resource "aws_s3_bucket_server_side_encryption_configuration" "s3_bucket_encryption" {
  bucket = aws_s3_bucket.terraform-capstone-s3.id

  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = aws_kms_key.terraform_capstone_s3_key.arn
      sse_algorithm     = "aws:kms"
    }

    # Reduces KMS costs and API traffic significantly
    bucket_key_enabled = true
  }
}