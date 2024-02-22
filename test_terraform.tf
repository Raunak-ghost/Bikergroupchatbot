provider "aws" {
  region = "ap-south-1"
  access_key = "AKIAYS2NSJVQVY35R7FZ"
  secret_key = "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"
}

output "role_arn" {
  value = aws_iam_role.lambda_role.arn
}

# IAM role for lambda instance
resource "aws_iam_role" "lambda_role" {
  name = "lambda_role"
  assume_role_policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Principal" : {
          "Service" : "lambda.amazonaws.com"
        },
        "Action" : "sts:AssumeRole"
      }
    ]
  })
}


# IAM policy for Lambda function
resource "aws_iam_policy" "lambda_policy" {
  name = "lambda_policy"
  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Action" : "lambda:InvokeFunction",
        "Resource" : "*",
      },
      {
        "Effect" : "Allow",
        "Action" : [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem"
        ],
        "Resource" : aws_dynamodb_table.example.arn
      }
    ]
  })
}

# Attach policy to IAM role
resource "aws_iam_role_policy_attachment" "lambda_attach" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}


# Lambda function
resource "aws_lambda_function" "test_lambda" {
  function_name = "test_lambda"
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.8"
  role          = aws_iam_role.lambda_role.arn
  filename = "lambda_function_payload.zip"
  source_code_hash = base64sha256(filebase64("lambda_function_payload.zip"))
}

# DynamoDB table
resource "aws_dynamodb_table" "example" {
  name           = "example"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "id"
  attribute {
    name = "id"
    type = "S"
  }
}

# EC2 instance
resource "aws_instance" "t2_instance" {
  ami = "ami-03f4878755434977f"  # Replace with the desired AMI ID
  instance_type = "t2.micro"
  key_name      = "newterraform"
}

