resource "aws_secretsmanager_secret" "this" {
  name                    = local.name
  recovery_window_in_days = 0
}

resource "aws_secretsmanager_secret_version" "this" {
  secret_id  = aws_secretsmanager_secret.this.id
  #depends_on = [aws_db_instance.this]

  secret_string = jsonencode({
    PROJECT_NAME                                        = local.name
    DATABASE_URL                                        = "postgresql://postgres:${random_password.database.result}@${aws_db_instance.this.endpoint}/${aws_db_instance.this.db_name}"
    ECR_PYTHON_REPOSITORY_URL                           = aws_ecr_repository.python.repository_url
    ECR_PYTHON_REPOSITORY_NAME                          = aws_ecr_repository.python.name
    BUCKET_FILES_DOMAIN_NAME                            = aws_s3_bucket.files.bucket_regional_domain_name
    API_FUNCTION_NAME                                   = aws_lambda_function.api.function_name
    DOCUMENT_PROCESSING_FUNCTION_NAME                   = aws_lambda_function.document_processing.function_name
    PAGE_RESULT_ANALYSIS_FUNCTION_NAME                  = aws_lambda_function.page_result_analysis.function_name
    COGNITO_PRE_SIGN_UP_FUNCTION_NAME                   = aws_lambda_function.cognito_pre_sign_up.function_name
    COGNITO_POST_CONFIRMATION_FUNCTION_NAME             = aws_lambda_function.cognito_post_confirmation.function_name
    INTERNAL_GATEWAY_ID                                 = aws_apigatewayv2_api.internal.id
    ENVIRONMENT                                         = local.environment
    AWS_S3_BUCKET_MY_ID                                 = aws_s3_bucket.my.id
    NEXT_PUBLIC_COGNITO_CLIENT_ID                       = aws_cognito_user_pool_client.this.id
    NEXT_PUBLIC_MY_DOMAIN_NAME                          = "https://${tolist(aws_cloudfront_distribution.my.aliases)[0]}"
    MY_DOMAIN_NAME                                      = "https://${tolist(aws_cloudfront_distribution.my.aliases)[0]}"
    VITE_MY_DOMAIN_NAME                                 = "https://${tolist(aws_cloudfront_distribution.my.aliases)[0]}"
    NEXT_PUBLIC_COGNITO_AUTH_DOMAIN_NAME                = "https://${aws_cognito_user_pool_domain.main.domain}"
    NEXT_PUBLIC_COGNITO_USER_POOL_ID                    = aws_cognito_user_pool.this.id
    MY_S3_BUCKET_DOMAIN_NAME                            = "https://${aws_s3_bucket.my.bucket_regional_domain_name}"
    NEXT_PUBLIC_INTERNAL_URL_DOMAIN_NAME                = "https://${aws_apigatewayv2_domain_name.internal.id}"
    BUCKET_WWW_ID                                       = aws_s3_bucket.www.id
    NEXT_PUBLIC_WWW_DOMAIN_NAME                         = "https://estructura.nietzscheson.com"
    GROQ_API_KEY = var.groq_api_key
  })
}

data "aws_secretsmanager_secret_version" "this" {
  secret_id  = aws_secretsmanager_secret.this.id
  depends_on = [aws_secretsmanager_secret.this]
}