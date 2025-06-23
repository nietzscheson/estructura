resource "aws_acm_certificate" "this" {
  domain_name       = "estructura.nietzscheson.com"
  validation_method = "DNS"

  subject_alternative_names = ["*.estructura.nietzscheson.com"]

  lifecycle {
    create_before_destroy = true
  }
}

#resource "aws_acm_certificate" "cloudfront" {
#  provider          = aws.us_east_1
#  domain_name       = "estructura.nietzcheson.com"
#  validation_method = "DNS"
#
#  subject_alternative_names = ["*.estructura.nietzscheson.com"]
#
#
#  lifecycle {
#    create_before_destroy = true
#  }
#}

resource "aws_apigatewayv2_domain_name" "internal" {
  domain_name = "internal.estructura.nietzscheson.com"

  domain_name_configuration {
    certificate_arn = aws_acm_certificate.this.arn
    endpoint_type   = "REGIONAL"
    security_policy = "TLS_1_2"
  }
}

resource "aws_apigatewayv2_api_mapping" "internal" {
  domain_name = aws_apigatewayv2_domain_name.internal.domain_name
  api_id      = aws_apigatewayv2_api.internal.id
  stage       = local.environment
}