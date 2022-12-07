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


def show_image(bucket):
    s3_client = boto3.client('s3', aws_access_key_id=my_id, aws_secret_access_key=my_secret_key)
    public_urls = []
    try:
        for item in s3_client.list_objects(Bucket=bucket)['Contents']:
            print("TEST>>>>>> item is", item)
            presigned_url = s3_client.generate_presigned_url(
                'get_object',
                Params = {'Bucket': bucket, 'Key': item['Key']},
                ExpiresIn = 100
            )
            public_urls.append(presigned_url)
    except Exception as e:
        print("ERROR: ", e)
        pass
    print("[INFO] : The contents inside show_image = ", public_urls)
    return public_urls
