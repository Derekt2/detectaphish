from aws_cdk import Stage
from constructs import Construct
from .frontend_stack import FrontendStack

class FrontendStage(Stage):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        FrontendStack(self, "FrontendStack", **kwargs)
