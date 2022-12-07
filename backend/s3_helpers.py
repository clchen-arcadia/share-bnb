import boto3
import os
from dotenv import load_dotenv

load_dotenv()

my_id = os.getenv('ACCESS_ID')
my_secret_key = os.getenv('ACCESS_KEY')


def upload_file(file_name, bucket):
    object_name = file_name
    s3_client = boto3.client('s3', aws_access_key_id=my_id, aws_secret_access_key=my_secret_key)
    response = s3_client.upload_file(file_name, bucket, object_name)
    return response
