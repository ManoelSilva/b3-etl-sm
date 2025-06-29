variable "lab_role_arn" {
  description = "ARN da role LabRole"
  type        = string
  default = "arn:aws:iam::861115334572:role/LabRole"
}

variable "bucket_name" {
  description = "Nome do bucket S3 para scripts do Glue."
  type        = string
  default = "861115334572-glue"
} 