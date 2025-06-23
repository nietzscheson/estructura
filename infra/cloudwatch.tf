resource "aws_cloudwatch_log_group" "api" {
  name              = "/aws/lambda/${local.name}-api"
  retention_in_days = local.environment == "dev" ? 1 : 7
}

resource "aws_cloudwatch_log_group" "cognito_post_confirmation" {
  name              = "/aws/lambda/${local.name}-cognito-post-confirmation"
  retention_in_days = local.environment == "dev" ? 1 : 7
}

resource "aws_cloudwatch_log_group" "cognito_pre_sign_up" {
  name              = "/aws/lambda/${local.name}-cognito-pre-sign-up"
  retention_in_days = local.environment == "dev" ? 1 : 7
}

resource "aws_cloudwatch_log_group" "document_processing" {
  name              = "/aws/lambda/${local.name}-document-processing"
  retention_in_days = local.environment == "dev" ? 1 : 7
}

resource "aws_cloudwatch_log_group" "trigger_state_machine" {
  name              = "/aws/lambda/${local.name}-trigger-state-machine"
  retention_in_days = local.environment == "dev" ? 1 : 7
}

resource "null_resource" "delete_log_streams_dev" {
  count = local.environment == "dev" ? 1 : 0

  provisioner "local-exec" {
    command     = <<EOT
      LOG_GROUPS=$(
        aws logs describe-log-groups --query "logGroups[?starts_with(logGroupName, '/aws/lambda/${local.name}')].logGroupName" --output text
      )
      for group in $LOG_GROUPS; do
        STREAMS=$(aws logs describe-log-streams --log-group-name "$group" --query "logStreams[].logStreamName" --output text)
        for stream in $STREAMS; do
          aws logs delete-log-stream --log-group-name "$group" --log-stream-name "$stream"
        done
      done
    EOT
    interpreter = ["/bin/bash", "-c"]
  }

  triggers = {
    always_run = timestamp()
  }
}
