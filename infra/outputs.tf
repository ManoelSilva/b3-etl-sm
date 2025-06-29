output "lambda_arn" {
  value = module.lambda.lambda_arn
}

output "step_function_arn" {
  value = module.step_function.step_function_arn
} 