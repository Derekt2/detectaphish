#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk_pipeline_stack.cdk_pipeline_stack import CdkPipelineStack
from cdk_pipeline_stack.frontend_infra_stack import FrontendInfraStack


app = cdk.App()

env = cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION'))

frontend_infra_stack = FrontendInfraStack(app, "FrontendInfraStack", env=env)

CdkPipelineStack(app, "CdkPipelineStack",
    frontend_bucket_name=frontend_infra_stack.frontend_bucket.bucket_name,
    distribution_id=frontend_infra_stack.distribution.distribution_id,
    env=env,
    # If you don't specify 'env', this stack will be environment-agnostic.
    # Account/Region-dependent features and context lookups will not work,
    # but a single synthesized template can be deployed anywhere.

    # Uncomment the next line to specialize this stack for the AWS Account
    # and Region that are implied by the current CLI configuration.

    #env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

    # Uncomment the next line if you know exactly what Account and Region you
    # want to deploy the stack to. */

    #env=cdk.Environment(account='123456789012', region='us-east-1'),

    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
    )

app.synth()
