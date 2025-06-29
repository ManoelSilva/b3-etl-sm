variable "glue_job_step1_name" {
  description = "Nome do Glue Job Step 1"
  type        = string
  default = "etl-step-1"
}

variable "glue_job_step2_name" {
  description = "Nome do Glue Job Step 2"
  type        = string
  default = "etl-step-2"
}

variable "glue_job_step3_name" {
  description = "Nome do Glue Job Step 3"
  type        = string
  default = "etl-step-3"
}

variable "lab_role_arn" {
  description = "ARN da role LabRole"
  type        = string
  default = "arn:aws:iam::861115334572:role/LabRole"
} 