variable "glue_extract_job_name" {
  description = "Name of the Glue Job Extraction Step"
  type        = string
  default = "b3-etl-extract-step"
}

variable "glue_transform_job_name" {
  description = "Name of the Glue Job Transformation Step"
  type        = string
  default = "b3-etl-transform-step"
}

variable "glue_load_job_name" {
  description = "Name of the Glue Job Load Step"
  type        = string
  default = "b3-etl-load-step"
}

variable "lab_role_arn" {
  description = "ARN of the LabRole role"
  type        = string
  default = "arn:aws:iam::861115334572:role/LabRole"
} 