# [infra/lambda_module/variables.tf](infra/lambda_module/variables.tf)

variable "lambda_zip_path" {
  description = "Path to the lambda zip file."
  type        = string
  default     = "../../lambda/build/start_step.zip"
}

variable "step_function_arn" {
  description = "ARN of the Step Function"
  type        = string
  default = "arn:aws:states:us-east-1:861115334572:stateMachine:b3-etl-step-function"
}

variable "lab_role_arn" {
  description = "ARN of the LabRole role"
  type        = string
  default = "arn:aws:iam::861115334572:role/LabRole"
} 