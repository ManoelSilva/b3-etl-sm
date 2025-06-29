variable "lambda_zip_path" {
  description = "Caminho para o arquivo zip da lambda."
  type        = string
  default     = "../../lambda/build/start_step.zip"
}

variable "step_function_arn" {
  description = "ARN da Step Function"
  type        = string
  default = "arn:aws:states:us-east-1:861115334572:stateMachine:etl-step-function"
}

variable "lab_role_arn" {
  description = "ARN da role LabRole"
  type        = string
  default = "arn:aws:iam::861115334572:role/LabRole"
} 