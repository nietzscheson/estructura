resource "aws_apigatewayv2_api" "internal" {
  name          = "${local.name}-internal"
  protocol_type = "HTTP"
  description   = "Estructura Application - Internal V2"

  depends_on = [aws_lambda_function.api]
}

resource "aws_apigatewayv2_integration" "internal" {
  api_id             = aws_apigatewayv2_api.internal.id
  integration_type   = "AWS_PROXY"
  integration_uri    = aws_lambda_function.api.invoke_arn
  integration_method = "POST"
}

resource "aws_apigatewayv2_route" "internal" {
  api_id    = aws_apigatewayv2_api.internal.id
  route_key = "ANY /{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.internal.id}"

  #authorization_type = "NONE"
  authorization_type = "JWT"
  authorizer_id      = aws_apigatewayv2_authorizer.cognito.id
}

resource "aws_lambda_permission" "internal" {
  statement_id  = "${local.name}-internal"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.api.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.internal.execution_arn}/*/*"
}

resource "aws_apigatewayv2_route" "internal_options" {
  api_id    = aws_apigatewayv2_api.internal.id
  route_key = "OPTIONS /{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.internal.id}"

  # ⚠️ Importante: sin autorización para permitir CORS preflight
  authorization_type = "NONE"
}

resource "aws_apigatewayv2_deployment" "internal" {
  api_id = aws_apigatewayv2_api.internal.id

  lifecycle {
    create_before_destroy = true
  }

  depends_on = [
    aws_apigatewayv2_route.internal,
    aws_apigatewayv2_route.internal_options
  ]
}

resource "aws_apigatewayv2_stage" "internal" {
  api_id        = aws_apigatewayv2_api.internal.id
  deployment_id = aws_apigatewayv2_deployment.internal.id
  name          = local.environment
  #auto_deploy  = true
}