resource "aws_cognito_user_pool" "this" {
  name                     = local.name
  username_attributes      = ["email"]
  auto_verified_attributes = ["email"]

  username_configuration {
    case_sensitive = false
  }

  email_configuration {
    email_sending_account = "COGNITO_DEFAULT"
  }

  password_policy {
    minimum_length                   = 6
    require_numbers                  = true
    require_symbols                  = true
    temporary_password_validity_days = 7
  }
  #  device_configuration {
  #    device_only_remembered_on_user_prompt = true
  #    challenge_required_on_new_device      = true
  #  }

  account_recovery_setting {
    recovery_mechanism {
      name     = "verified_email"
      priority = 1
    }
  }

  lambda_config {
    pre_sign_up       = aws_lambda_function.cognito_pre_sign_up.arn
    post_confirmation = aws_lambda_function.cognito_post_confirmation.arn
  }

}

resource "aws_cognito_user_pool_domain" "main" {
  domain          = "auth.estructura.nietzscheson.com"
  certificate_arn = aws_acm_certificate.this.arn
  user_pool_id    = aws_cognito_user_pool.this.id

  #managed_login_version = 2
}

locals {
  callback_urls = [
    "http://localhost:3000/auth/callback/",
    "https://my.estructura.nietzscheson.com/auth/callback/",
  ]

  logout_urls = [
    "http://localhost:3000",
    "http://localhost:3001",
    "https://my.estructura.nietzscheson.com"
  ]
}

resource "aws_cognito_user_pool_client" "this" {
  name                 = local.name
  user_pool_id         = aws_cognito_user_pool.this.id
  allowed_oauth_flows  = ["code"]
  allowed_oauth_scopes = ["email", "openid", "profile", "aws.cognito.signin.user.admin"]
  # generate_secret                      = true
  allowed_oauth_flows_user_pool_client = true
  # allowed_oauth_flows                  = ["implicit"] # code
  # allowed_oauth_scopes                 = ["email", "openid"]
  prevent_user_existence_errors = "ENABLED"
  supported_identity_providers  = ["COGNITO", "Google"]
  # # TODO: What if prod is on a custom domain?
  callback_urls = local.callback_urls
  logout_urls   = local.logout_urls

  explicit_auth_flows = ["ALLOW_CUSTOM_AUTH", "ALLOW_REFRESH_TOKEN_AUTH", "ALLOW_USER_PASSWORD_AUTH", "ALLOW_USER_SRP_AUTH", "ALLOW_ADMIN_USER_PASSWORD_AUTH"]
}

resource "aws_cognito_identity_provider" "google" {
  user_pool_id  = aws_cognito_user_pool.this.id
  provider_name = "Google"
  provider_type = "Google"

  provider_details = {
    authorize_scopes = "email"
    client_id     = var.google_client_id
    client_secret = var.google_client_secret
  }

  attribute_mapping = {
    email    = "email"
    username = "sub"
  }
}

resource "aws_cognito_managed_user_pool_client" "this" {
  name_prefix  = local.name
  user_pool_id = aws_cognito_user_pool.this.id
}

#resource "null_resource" "delete_all_users" {
#  #count = local.environment == "dev" ? 1 : 0
#
#  provisioner "local-exec" {
#    command = <<EOT
#USERS=$(aws cognito-idp list-users --user-pool-id ${aws_cognito_user_pool.this.id} --query "Users[*].Username" --output text)
#for USER in $USERS; do
#  echo "Deleting $USER"
#  aws cognito-idp admin-delete-user --user-pool-id ${aws_cognito_user_pool.this.id} --username "$USER"
#done
#EOT
#  }
#
#  triggers = {
#    always_run = timestamp()
#  }
#}
#