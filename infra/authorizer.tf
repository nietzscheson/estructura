resource "aws_apigatewayv2_authorizer" "cognito" {
  name            = "${local.name}-cognito-authorizer"
  api_id          = aws_apigatewayv2_api.internal.id
  authorizer_type = "JWT"

  identity_sources = ["$request.header.Authorization"]

  jwt_configuration {
    audience = [aws_cognito_user_pool_client.this.id]
    #issuer   = "https://${aws_cognito_user_pool.this.endpoint}"
    issuer = "https://cognito-idp.${var.aws_default_region}.amazonaws.com/${aws_cognito_user_pool.this.id}"

  }
}