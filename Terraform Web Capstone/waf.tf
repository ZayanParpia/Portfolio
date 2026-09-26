#WAF CONFIG

resource "aws_wafv2_web_acl" "terraform_capstone_web_acl" {
  name        = "terraform-capstone-web-acl"
  description = "WAF for my Terraform Capstone project"
  scope       = "REGIONAL"

  default_action {
    allow {}
  }

  visibility_config {
    cloudwatch_metrics_enabled = true
    metric_name                = "basicWebACLMetric"
    sampled_requests_enabled   = true
  }

  rule {
    name     = "RateLimitRule"
    priority = 1

    action {
      block {}
    }

    statement {
      rate_based_statement {
        limit              = 2000
        aggregate_key_type = "IP"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "RateLimitRuleMetric"
      sampled_requests_enabled   = true
    }
  }
}

resource "aws_wafv2_web_acl_association" "terraform_capstone_web_acl_association" {
  resource_arn = "${aws_lb.Terraform_ALB.arn}"
  web_acl_arn  = aws_wafv2_web_acl.terraform_capstone_web_acl.arn
}