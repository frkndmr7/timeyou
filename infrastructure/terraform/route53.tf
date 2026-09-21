resource "aws_route53_zone" "timeyou" {
  name = "timeyou.co"
}

data "aws_lb" "timeyou_dev" {
  count = var.manage_production_alias ? 1 : 0

  tags = {
    "ingress.k8s.aws/stack" = "timeyou-prod/timeyou"
  }
}

resource "aws_route53_record" "timeyou_apex" {
  count = var.manage_production_alias ? 1 : 0

  zone_id = aws_route53_zone.timeyou.zone_id
  name    = "timeyou.co"
  type    = "A"

  alias {
    name                   = data.aws_lb.timeyou_dev[0].dns_name
    zone_id                = data.aws_lb.timeyou_dev[0].zone_id
    evaluate_target_health = true
  }
}

moved {
  from = aws_route53_record.timeyou_apex
  to   = aws_route53_record.timeyou_apex[0]
}
