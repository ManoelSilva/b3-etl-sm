variable "glue_extract_job_name" {
  description = "Nome do Glue Job Step de Extração"
  type        = string
  default = "etl-extract-step"
}

variable "glue_transform_job_name" {
  description = "Nome do Glue Job Step de Transformação"
  type        = string
  default = "etl-transform-step"
}

variable "glue_load_job_name" {
  description = "Nome do Glue Job Step de Carregamento"
  type        = string
  default = "etl-load-step"
}

variable "lab_role_arn" {
  description = "ARN da role LabRole"
  type        = string
  default = "arn:aws:iam::861115334572:role/LabRole"
} 