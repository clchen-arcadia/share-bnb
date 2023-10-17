import boto3
import os
from dotenv import load_dotenv

load_dotenv()

my_id = os.getenv('ACCESS_ID')
my_secret_key = os.getenv('ACCESS_KEY')
my_region = os.getenv('REGION_NAME')

EXPIRE_TIME = 500


def upload_file(file_name, bucket):
    object_name = file_name
    s3_client = boto3.client(
        's3',
        region_name=my_region,
        aws_access_key_id=my_id,
        aws_secret_access_key=my_secret_key)
    response = s3_client.upload_file(file_name, bucket, object_name)
    return response


def get_all_urls_from_s3(bucket):
    s3_client = boto3.client(
        's3',
        region_name=my_region,
        aws_access_key_id=my_id,
        aws_secret_access_key=my_secret_key
    )
    public_urls = []
    try:
        # item as : item is {
        # 'Key': 'uploads/cute-dog-headshot.jpeg',
        # 'LastModified': datetime.datetime(2022, 12, 7, 22, 8, 31, tzinfo=tzutc()),
        # 'ETag': '"9ac99555c1f3e7c21df8db7351ae9ab5"',
        # 'Size': 277860,
        # 'StorageClass': 'STANDARD',
        # 'Owner': {
        #   'DisplayName': 'clchen.arcadia',
        #   'ID': '570d641f3d2fe3e75ee4635997a6a72d488b4e1e4a6c64553166156329f1a0dd'
        #   }
        # }
        for item in s3_client.list_objects(Bucket=bucket)['Contents']:
            print("TEST>>>>>> item is", item)
            presigned_url = s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket, 'Key': item['Key']},
                ExpiresIn=EXPIRE_TIME
            )
            public_urls.append(presigned_url)
    except Exception as e:
        print("ERROR: ", e)
        pass
    print("[INFO] : The contents inside show_image = ", public_urls)
    return public_urls

def get_image_url(bucket, key):

    s3_client = boto3.client(
        's3',
        region_name=my_region,
        aws_access_key_id=my_id,
        aws_secret_access_key=my_secret_key)

    try:

        presigned_url = s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket, 'Key': key},
                ExpiresIn=EXPIRE_TIME
            )
    except Exception as e:
        print("ERROR: ", e)
        pass
    return presigned_url
