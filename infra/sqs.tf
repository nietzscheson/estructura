resource "aws_sqs_queue" "document_processing" {
  name = "${local.name}-document-processing"
}

resource "aws_lambda_event_source_mapping" "document_processing" {
  event_source_arn                   = aws_sqs_queue.document_processing.arn
  function_name                      = aws_lambda_function.document_processing.arn
  batch_size                         = 1
  maximum_batching_window_in_seconds = 1
  enabled                            = true
}