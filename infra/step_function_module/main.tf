resource "aws_sfn_state_machine" "etl" {
  name     = "b3-etl-step-function"
  role_arn = var.lab_role_arn
  definition = jsonencode({
    StartAt = "Extract",
    States = {
      Extract = {
        Type     = "Task",
        Resource = "arn:aws:states:::glue:startJobRun.sync",
        Parameters = {
          JobName = var.glue_extract_job_name
        },
        Next = "Transform"
      },
      Transform = {
        Type     = "Task",
        Resource = "arn:aws:states:::glue:startJobRun.sync",
        Parameters = {
          JobName = var.glue_transform_job_name
        },
        Next = "Load"
      },
      Load = {
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