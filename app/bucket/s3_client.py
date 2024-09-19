# s3_client.py
import boto3
from app.configs import CREDENTIALS_ACCESS_KEY, CREDENTIALS_SECRET_KEY

client_s3 = boto3.client(
    's3',
    aws_access_key_id=CREDENTIALS_ACCESS_KEY,
    aws_secret_access_key=CREDENTIALS_SECRET_KEY,
)
