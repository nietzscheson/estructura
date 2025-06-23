resource "aws_ecr_repository" "python" {
  name                 = "${local.name}-python"
  image_tag_mutability = "MUTABLE"
  force_delete         = true

  image_scanning_configuration {
    scan_on_push = true
  }

  lifecycle {
    ignore_changes        = all
    create_before_destroy = true
  }
}

resource "aws_ecr_lifecycle_policy" "python" {
  repository = aws_ecr_repository.python.name

  policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Keep last 3 images"
        selection = {
          tagStatus   = "any"
          countType   = "imageCountMoreThan"
          countNumber = 3
        }
        action = {
          type = "expire"
        }
      }
    ]
  })
}

resource "null_resource" "python" {
  provisioner "local-exec" {
    command = <<-EOF
      if [ $(aws ecr list-images --repository-name ${aws_ecr_repository.python.name} --region ${var.aws_default_region} | jq '.imageIds | length') -gt 0 ]; then
        echo "Repository has content, skipping."
      else
        echo "Repository is empty, executing commands."
        aws ecr get-login-password --region ${var.aws_default_region} | docker login -u AWS --password-stdin ${data.aws_caller_identity.current.account_id}.dkr.ecr.${var.aws_default_region}.amazonaws.com
        docker pull alpine
        docker tag alpine ${aws_ecr_repository.python.repository_url}:latest
        docker push ${aws_ecr_repository.python.repository_url}:latest
      fi
    EOF
  }

  triggers = {
    "run_at" = timestamp()
  }

  depends_on = [
    aws_ecr_repository.python,
    aws_ecr_lifecycle_policy.python,
  ]
}