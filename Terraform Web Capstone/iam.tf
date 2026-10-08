# ============================================================
# EC2 IAM ROLE
# SSM + S3
# ============================================================

# Trust policy: allow EC2 to assume this role
data "aws_iam_policy_document" "ec2_assume_role" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "ec2_role" {
  name               = "test-ec2-role"
  assume_role_policy = data.aws_iam_policy_document.ec2_assume_role.json
}


# ============================================================
# SSM PERMISSIONS
# ============================================================

resource "aws_iam_role_policy_attachment" "ssm_managed" {
  role       = aws_iam_role.ec2_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}


# ============================================================
# S3 PERMISSIONS
# ============================================================

resource "aws_iam_role_policy" "s3_access" {
  name = "EC2-S3-Access"
  role = aws_iam_role.ec2_role.id

  policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Sid      = "ListBucket"
        Effect   = "Allow"
        Action   = ["s3:ListBucket"]
        Resource = aws_s3_bucket.terraform-capstone-s3.arn
      },
      {
        Sid    = "ReadWriteObjects"
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:AbortMultipartUpload"
        ]
        Resource = "${aws_s3_bucket.terraform-capstone-s3.arn}/*"
      },
      {
        Sid    = "KmsForBucketEncryption"
        Effect = "Allow"
        Action = [
          "kms:GenerateDataKey",
          "kms:Decrypt"
        ]
        Resource = aws_kms_key.terraform_capstone_s3_key.arn
      }
    ]
  })
}


# ============================================================
# EC2 INSTANCE PROFILE
# ============================================================

resource "aws_iam_instance_profile" "ec2_profile" {
  name = "EC2-Instance-Profile"
  role = aws_iam_role.ec2_role.name
}


# ============================================================
# ALB LOGS
# ============================================================


# data "aws_iam_policy_document" "alb_logs" {
#   statement {
#     sid    = "AllowALBLogDelivery"
#     effect = "Allow"

#     principals {
#       type        = "Service"
#       identifiers = ["logdelivery.elasticloadbalancing.amazonaws.com"]
#     }

#     actions   = ["s3:PutObject"]
#     resources = ["${aws_s3_bucket.terraform-capstone-s3-alb-logs.arn}/alb/AWSLogs/${data.aws_caller_identity.current.account_id}/*"]

#     condition {
#       test     = "StringEquals"
#       variable = "s3:x-amz-acl"
#       values   = ["bucket-owner-full-control"]
#     }
#   }
# }

data "aws_caller_identity" "current" {}

# ============================================================
# Flow Log IAM role and policy
# ============================================================
resource "aws_cloudwatch_log_group" "terraform_capstone_flow_log_group" {
  name              = "terraform-capstone-flow-logs"
  retention_in_days = 14
    tags = {
    Name = "terraform-capstone-flow-logs"
  }
}

data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["vpc-flow-logs.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "terraform_capstone_flow_log_role" {
  name               = "terraform-capstone-flow-log-role"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

data "aws_iam_policy_document" "terraform_capstone_flow_log_policy" {
  statement {
    effect = "Allow"

    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
      "logs:DescribeLogGroups",
      "logs:DescribeLogStreams",
    ]

    resources = ["${aws_cloudwatch_log_group.terraform_capstone_flow_log_group.arn}:*"]
  }
}

resource "aws_iam_role_policy" "terraform_capstone_flow_log_policy" {
  name   = "terraform-capstone-flow-log-policy"
  role   = aws_iam_role.terraform_capstone_flow_log_role.id
  policy = data.aws_iam_policy_document.terraform_capstone_flow_log_policy.json
}

