from constructs import Construct
from aws_cdk import (
    Stack,
    SecretValue,
    aws_s3 as s3,
    aws_s3_deployment as s3_deployment,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_cloudfront as cloudfront,
    aws_route53 as route53,
    aws_route53_targets as route53_targets,
    aws_certificatemanager as acm,
    pipelines,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    aws_codebuild as codebuild,
)
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep, CodeBuildStep
from .pipeline_stage import PipelineStage
from aws_cdk import aws_iam as iam


class CdkPipelineStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, frontend_bucket_name: str, distribution_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Defines the source of our code, in this case a GitHub repository
        source = CodePipelineSource.git_hub(
            "Derekt2/detectaphish", "main",
            authentication=SecretValue.secrets_manager("github-token2")
        )

        pipeline = CodePipeline(self, "Pipeline",
            pipeline_name="MyPipeline",
            synth=ShellStep("Synth",
                input=source,
                commands=["npm install -g aws-cdk",
                          "python -m pip install -r requirements.txt",
                          "cdk synth"]
            )
        )

        # Backend Deploy Stage
        backend_deploy = PipelineStage(self, "BackendDeploy", env=kwargs["env"])

        # Frontend Build
        frontend_build = ShellStep("FrontendBuild",
            input=source,
            commands=[
                "cd frontend",
                "npm install",
                "npm run build"
            ],
            primary_output_directory="frontend/dist"
        )
        
        # Frontend Deploy Step
        frontend_deploy_step = CodeBuildStep("DeployFrontend",
            input=frontend_build.primary_output,
            commands=[f"aws s3 sync . s3://{frontend_bucket_name}"],
            role_policy_statements=[
                iam.PolicyStatement(
                    actions=["s3:ListBucket"],
                    resources=[f"arn:aws:s3:::{frontend_bucket_name}"]
                ),
                iam.PolicyStatement(
                    actions=["s3:PutObject", "s3:DeleteObject"],
                    resources=[f"arn:aws:s3:::{frontend_bucket_name}/*"]
                )
            ]
        )

        # Add a single wave for deployment, running backend and frontend in parallel
        deploy_wave = pipeline.add_wave("Deploy")
        deploy_wave.add_stage(backend_deploy)
        deploy_wave.add_post(frontend_build, frontend_deploy_step)
        
        # Invalidate CloudFront cache
        invalidation_step = CodeBuildStep("InvalidateCache",
            input=frontend_build.primary_output,
            commands=[
                f"aws cloudfront create-invalidation --distribution-id {distribution_id} --paths '/*'"
            ],
            role_policy_statements=[
                iam.PolicyStatement(
                    actions=["cloudfront:CreateInvalidation"],
                    resources=[f"arn:aws:cloudfront::{self.account}:distribution/{distribution_id}"]
                )
            ]
        )
        deploy_wave.add_post(invalidation_step)
