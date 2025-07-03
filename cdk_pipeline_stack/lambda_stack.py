from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_route53 as route53,
    aws_route53_targets as targets,
    aws_certificatemanager as acm,
)
from constructs import Construct

class LambdaStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        my_lambda = _lambda.Function(
            self, 'HelloHandler',
            runtime=_lambda.Runtime.PYTHON_3_12,
            code=_lambda.Code.from_asset('lambda'),
            handler='app.handler',
        )

        # Look up the hosted zone
        hosted_zone = route53.HostedZone.from_lookup(
            self, "HostedZone",
            domain_name="detectaphish.com"
        )

        # Create a certificate
        certificate = acm.Certificate(
            self, "Certificate",
            domain_name="api.detectaphish.com",
            validation=acm.CertificateValidation.from_dns(hosted_zone),
        )

        # Create the API Gateway Domain Name
        domain_name = apigw.DomainName(
            self, "ApiDomainName",
            domain_name="api.detectaphish.com",
            certificate=certificate,
            endpoint_type=apigw.EndpointType.REGIONAL
        )

        # Create the API Gateway
        api = apigw.LambdaRestApi(
            self, 'Endpoint',
            handler=my_lambda,
            default_cors_preflight_options=apigw.CorsOptions(
                allow_origins=apigw.Cors.ALL_ORIGINS,
                allow_methods=apigw.Cors.ALL_METHODS
            ),
            binary_media_types=["*/*"]
        )

        # Map the domain name to the API
        apigw.BasePathMapping(
            self, "ApiBasePathMapping",
            domain_name=domain_name,
            rest_api=api
        )

        # Create a Route53 record
        route53.ARecord(
            self, "AliasRecord",
            zone=hosted_zone,
            record_name="api",
            target=route53.RecordTarget.from_alias(targets.ApiGatewayDomain(domain_name))
        )
