import boto3
from django.conf import settings


def s3_client():
    s3_client = boto3.client(
        's3',
        aws_access_key_id = settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY,
        region_name = settings.AWS_S3_REGION_NAME,
    )
    return s3_client