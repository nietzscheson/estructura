resource "null_resource" "alembic_migrations" {

  #count = local.environment == "dev" ? 1 : 0

  triggers = {
    always_run  = timestamp() # fuerza ejecución cada vez (solo para desarrollo)
    db_url_hash = sha1(jsondecode(data.aws_secretsmanager_secret_version.this.secret_string)["DATABASE_URL"])
  }

  provisioner "local-exec" {
    environment = {
      DATABASE_URL = jsondecode(data.aws_secretsmanager_secret_version.this.secret_string)["DATABASE_URL"]
    }
    #command = "set -e && poetry run alembic downgrade base && poetry run alembic upgrade head"
    command     = "set -e && poetry run alembic upgrade head"
    working_dir = "${path.module}/../core/"
  }
}

resource "aws_lambda_function" "api" {
  function_name = "${local.name}-api"
  image_uri     = "${aws_ecr_repository.python.repository_url}:latest"
  depends_on    = [aws_ecr_repository.python, null_resource.alembic_migrations, aws_cloudwatch_log_group.api]
  role          = aws_iam_role.default.arn
  package_type  = "Image"

  environment {
    variables = local.secrets
  }

  image_config {
    command = ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
  }

  timeout     = 30
  memory_size = 512
}

resource "aws_lambda_function" "document_processing" {
  function_name = "${local.name}-document-processing"
  image_uri     = "${aws_ecr_repository.python.repository_url}:latest"
  depends_on    = [aws_ecr_repository.python, aws_cloudwatch_log_group.document_processing]
  role          = aws_iam_role.default.arn
  package_type  = "Image"

  environment {
    variables = local.secrets
  }

  image_config {
    entry_point = ["/usr/local/bin/python", "-m", "awslambdaric"]
    command     = ["src.handlers.document_processing.handler"]
  }

  timeout     = 30
  memory_size = 515
}


resource "aws_lambda_function" "page_result_analysis" {
  function_name = "${local.name}-page-result-analysis"
  image_uri     = "${aws_ecr_repository.python.repository_url}:latest"
  depends_on    = [aws_ecr_repository.python]
  role          = aws_iam_role.default.arn
  package_type  = "Image"

  environment {
    variables = local.secrets
  }

  image_config {
    entry_point = ["/usr/local/bin/python", "-m", "awslambdaric"]
    command     = ["src.handlers.page_result_analysis.handler"]
  }

  timeout     = 900
  memory_size = 512

}

resource "aws_lambda_function" "cognito_pre_sign_up" {
  function_name = "${local.name}-cognito-pre-sign-up"
  image_uri     = "${aws_ecr_repository.python.repository_url}:latest"
  depends_on    = [aws_ecr_repository.python]
  role          = aws_iam_role.default.arn
  package_type  = "Image"

  image_config {
    entry_point = ["/usr/local/bin/python", "-m", "awslambdaric"]
    command     = ["src.handlers.cognito_pre_sign_up.handler"]
  }

  environment {
    variables = local.secrets
  }

  timeout     = 10
  memory_size = 256
}

resource "aws_lambda_permission" "allow_cognito" {
  statement_id  = "AllowExecutionFromCognito"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.cognito_pre_sign_up.function_name
  principal     = "cognito-idp.amazonaws.com"
  source_arn    = aws_cognito_user_pool.this.arn
}


resource "aws_lambda_function" "cognito_post_confirmation" {
  function_name = "${local.name}-cognito-post-confirmation"
  image_uri     = "${aws_ecr_repository.python.repository_url}:latest"
  depends_on    = [aws_ecr_repository.python]
  role          = aws_iam_role.default.arn
  package_type  = "Image"

  image_config {
    entry_point = ["/usr/local/bin/python", "-m", "awslambdaric"]
    command     = ["src.handlers.cognito_post_confirmation.handler"]
  }

  timeout     = 10
  memory_size = 256

  environment {
    variables = local.secrets
  }
}

resource "aws_lambda_permission" "allow_cognito_post_confirmation" {
  statement_id  = "AllowExecutionFromCognito"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.cognito_post_confirmation.function_name
  principal     = "cognito-idp.amazonaws.com"
  source_arn    = aws_cognito_user_pool.this.arn
}