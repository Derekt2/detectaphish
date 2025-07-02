# Python Lambda with CDK and CodePipeline


[View Pipeline in AWS Console](https://console.aws.amazon.com/codesuite/codepipeline/pipelines/MyPipeline/view)

This project demonstrates how to deploy a Python Lambda function using the AWS CDK and a CodePipeline for continuous deployment.

## Prerequisites

* AWS Account and AWS CLI configured
* Node.js and npm installed
* Python 3.9+ installed
* Git installed

## Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repository-url>
   cd <your-repository-name>
   ```

2. **Create a GitHub token:**
   - Go to your GitHub account settings > Developer settings > Personal access tokens.
   - Generate a new token with the `repo` and `workflow` scopes.
   - Store this token in AWS Secrets Manager as a plaintext secret named `github-token`.

   You can create the secret using the AWS CLI with the following command:
   ```bash
   aws secretsmanager create-secret --name github-token --secret-string <your-github-token>
   ```

3. **Update the pipeline configuration:**
   - Open `cdk_pipeline_stack/cdk_pipeline_stack.py`.
   - Replace `"OWNER/REPO"` with your GitHub username and repository name.

4. **Install dependencies:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

## Deployment

1. **Bootstrap your AWS account for CDK:**
   ```bash
   cdk bootstrap
   ```

2. **Deploy the CDK stack:**
   ```bash
   cdk deploy
   ```

This will create the CodePipeline, which will then build and deploy your Lambda function. Any subsequent pushes to the `main` branch will automatically trigger a new deployment.

## Lambda Function

The Lambda function is located in the `lambda` directory. It's a simple function that returns a "Hello from Lambda!" message. The API Gateway endpoint will be created as part of the deployment, and you can find the URL in the AWS CloudFormation console output for the `LambdaStack`.

## Local Testing

You can test the Lambda function locally using the AWS SAM CLI.

1. **Synthesize the CloudFormation template:**
   ```bash
   cdk synth
   ```

2. **Invoke the function locally:**
   ```bash
   sudo sam local invoke HelloHandler -t cdk.out/assembly-CdkPipelineStack-Deploy/CdkPipelineStackDeployLambdaStack85B16C90.template.json
   ```
   *Note: `sudo` may be required to allow SAM to access the Docker daemon.*
