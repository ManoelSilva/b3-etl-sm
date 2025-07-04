variable "lab_role_arn" {
  description = "ARN of the LabRole role"
  type        = string
  default = "arn:aws:iam::861115334572:role/LabRole"
}

variable "bucket_name" {
  description = "Name of the S3 bucket for Glue scripts."
  type        = string
  default = "861115334572-glue"
}

variable "refined_bucket_name" {
  description = "Nome do bucket S3 refined."
  type        = string
  default     = "861115334572-refined"
} 