locals {
  name               = "estructura-${terraform.workspace}"
  environment        = terraform.workspace
  account_id         = data.aws_caller_identity.current.account_id
  domain_name_prefix = terraform.workspace == "dev" ? "api.dev" : "api"
  domain_name        = "estructura.nietzscheson.com"

  secrets = jsondecode(data.aws_secretsmanager_secret_version.this.secret_string)
}

data "aws_caller_identity" "current" {}

#variable "region" {
#  default = "us-east-1"
#  description = "The AWS region to create resources in."
#}

variable "aws_default_region" {
  description = "The AWS region to create resources in."
  default = "us-east-1"
}

variable "groq_api_key" {}

variable "stripe_api_key" {}

variable "google_client_id" {}
variable "google_client_secret" {}