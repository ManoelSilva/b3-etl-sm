resource "aws_sfn_state_machine" "etl" {
  name     = "etl-step-function"
  role_arn = var.lab_role_arn
  definition = jsonencode({
    StartAt = "Step1",
    States = {
      Step1 = {
        Type     = "Task",
        Resource = "arn:aws:states:::glue:startJobRun.sync",
        Parameters = {
          JobName = var.glue_job_step1_name
        },
        Next = "Step2"
      },
      Step2 = {
        Type     = "Task",
        Resource = "arn:aws:states:::glue:startJobRun.sync",
        Parameters = {
          JobName = var.glue_job_step2_name
        },
        Next = "Step3"
      },
      Step3 = {
        Type     = "Task",
        Resource = "arn:aws:states:::glue:startJobRun.sync",
        Parameters = {
          JobName = var.glue_job_step3_name
        },
        End = true
      }
    }
  })
}

output "step_function_arn" {
  value = aws_sfn_state_machine.etl.arn
} 