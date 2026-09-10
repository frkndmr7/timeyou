resource "aws_route53_zone" "timeyou" {
  name = "timeyou.co"
}

data "aws_lb" "timeyou_dev" {
  tags = {
    "ingress.k8s.aws/stack" = "timeyou-prod/timeyou"
  }
}

resource "aws_route53_record" "timeyou_apex" {
  zone_id = aws_route53_zone.timeyou.zone_id
  name    = "timeyou.co"
  type    = "A"

  alias {
    name                   = data.aws_lb.timeyou_dev.dns_name
    zone_id                = data.aws_lb.timeyou_dev.zone_id
    evaluate_target_health = true
  }
}
