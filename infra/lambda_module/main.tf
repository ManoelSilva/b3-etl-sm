resource "aws_lambda_function" "etl_trigger" {
  function_name = "b3_etl_s3_trigger"
  handler       = "start_step.lambda_handler"
  runtime       = "python3.12"
  role          = var.lab_role_arn
  filename      = var.lambda_zip_path
  source_code_hash = filebase64sha256(var.lambda_zip_path)
  environment {
    variables = {
      STEP_FUNCTION_ARN = var.step_function_arn
    }
  }
}

resource "aws_lambda_permission" "allow_s3" {
  statement_id  = "AllowExecutionFromS3"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.etl_trigger.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = "arn:aws:s3:::861115334572-raw"
}

resource "aws_s3_bucket_notification" "trigger_lambda" {
  bucket = "861115334572-raw"
  lambda_function {
    lambda_function_arn = aws_lambda_function.etl_trigger.arn
    events              = ["s3:ObjectCreated:*"]
  }
  depends_on = [aws_lambda_permission.allow_s3]
}

output "lambda_arn" {
  value = aws_lambda_function.etl_trigger.arn
} 