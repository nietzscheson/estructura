provider "aws" {
  region = var.aws_default_region
  default_tags {
    tags = {
      Name        = local.name
      Environment = local.environment
    }
  }
}

provider "aws" {
  alias  = "us_east_1"
  region = "us-east-1"

  default_tags {
    tags = {
      Name        = local.name
      Environment = local.environment
    }
  }

}

terraform {
  backend "s3" {
    bucket = "estructura-project"
    key    = "state.tfstate"
    region = "us-east-1"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.95.0"
    }
  }
}