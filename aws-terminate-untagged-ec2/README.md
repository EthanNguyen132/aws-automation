# Lambda function to terminate ec2 with im-proper tagging for PC-Code ([a-z,A-Z,0-9]{4})
## To run lambda locally (requires python-lambda-local)

`
python-lambda-local  -f lambda_handler  lambda_function.py cloudtrail_event.json
`

## IAM role for lambda (managed + custom policy)

```
arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
```

```
Version: "2012-10-17"
Statement: 
 - 
  Sid: AllowDescribeAndTerminateInstance
  Effect: Allow
  Action: 
   - "ec2:DescribeInstances"
   - "ec2:TerminateInstances"
  Resource: "*"


Allow lambda to terminate improper tagged ec2 instances
```