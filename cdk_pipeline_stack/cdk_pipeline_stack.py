from constructs import Construct
from aws_cdk import (
    Stack,
    SecretValue,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
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
