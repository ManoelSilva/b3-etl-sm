resource "aws_sfn_state_machine" "etl" {
  name     = "b3-etl-step-function"
  role_arn = var.lab_role_arn
  definition = jsonencode({
    StartAt = "B3Extract",
    States = {
      B3Extract = {
        Type     = "Task",
        Resource = "arn:aws:states:::glue:startJobRun.sync",
        Parameters = {
          JobName = var.glue_extract_job_name
        },
        Next = "B3Transform"
      },
      B3Transform = {
        Type     = "Task",
        Resource = "arn:aws:states:::glue:startJobRun.sync",
        Parameters = {
          JobName = var.glue_transform_job_name
        },
        Next = "B3Load"
      },
      B3Load = {
        Type     = "Task",
        Resource = "arn:aws:states:::glue:startJobRun.sync",
        Parameters = {
          JobName = var.glue_load_job_name
        },
        End = true
      }
    }
  })
}

output "step_function_arn" {
  value = aws_sfn_state_machine.etl.arn
} 