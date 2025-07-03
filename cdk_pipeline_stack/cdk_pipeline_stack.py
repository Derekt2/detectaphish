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
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep
from .pipeline_stage import PipelineStage


class CdkPipelineStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
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

        deploy = PipelineStage(self, "Deploy", env=kwargs["env"])
        deploy_stage = pipeline.add_stage(deploy)

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

        # Frontend Deploy
        deploy.add_pre(frontend_build)
        
        frontend_bucket = s3.Bucket(self, "FrontendBucket",
            website_index_document="index.html",
            public_read_access=True,
            block_public_access=s3.BlockPublicAccess(block_public_policy=False)
        )

        s3_deployment.BucketDeployment(self, "DeployFrontend",
            sources=[s3_deployment.Source.asset("frontend/dist")],
            destination_bucket=frontend_bucket
        )

        # Look up the hosted zone
        hosted_zone = route53.HostedZone.from_lookup(
            self, "HostedZone",
            domain_name="detectaphish.com"
        )

        # Create a certificate for the frontend
        frontend_certificate = acm.Certificate(
            self, "FrontendCertificate",
            domain_name="detectaphish.com",
            validation=acm.CertificateValidation.from_dns(hosted_zone),
        )

        # Create a CloudFront distribution
        distribution = cloudfront.Distribution(
            self, "FrontendDistribution",
            default_behavior=cloudfront.BehaviorOptions(
                origin=cloudfront.S3Origin(frontend_bucket),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
            ),
            domain_names=["detectaphish.com"],
            certificate=frontend_certificate,
            default_root_object="index.html",
        )

        # Create a Route53 record
        route53.ARecord(
            self, "FrontendAliasRecord",
            zone=hosted_zone,
            record_name="detectaphish.com",
            target=route53.RecordTarget.from_alias(route53_targets.CloudFrontTarget(distribution))
        )
