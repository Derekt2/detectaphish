from aws_cdk import (
    Stack,
    CfnOutput,
    aws_s3 as s3,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as cloudfront_origins,
    aws_route53 as route53,
    aws_route53_targets as route53_targets,
    aws_certificatemanager as acm,
)
from constructs import Construct

class FrontendInfraStack(Stack):
    @property
    def frontend_bucket(self):
        return self._frontend_bucket

    @property
    def distribution(self):
        return self._distribution

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self._frontend_bucket = s3.Bucket(self, "FrontendBucket",
            website_index_document="index.html",
            public_read_access=True,
            block_public_access=s3.BlockPublicAccess(block_public_policy=False)
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
        self._distribution = cloudfront.Distribution(
            self, "FrontendDistribution",
            default_behavior=cloudfront.BehaviorOptions(
                origin=cloudfront_origins.S3Origin(self._frontend_bucket),
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
            target=route53.RecordTarget.from_alias(route53_targets.CloudFrontTarget(self._distribution))
        )

        CfnOutput(self, "DistributionId", value=self._distribution.distribution_id)
