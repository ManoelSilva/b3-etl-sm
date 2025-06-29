import os
import boto3
import json

def lambda_handler(event, context):
    sfn = boto3.client('stepfunctions')
    step_function_arn = os.environ['STEP_FUNCTION_ARN']
    sfn.start_execution(
        stateMachineArn=step_function_arn,
        input=json.dumps(event)
    )
    return {'status': 'Step Function started'}