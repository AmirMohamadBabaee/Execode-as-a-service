import os
import boto3
from botocore.exceptions import ClientError


LIARA_ENDPOINT="https://storage.iran.liara.space"
LIARA_BUCKET_NAME="awesome-curie-tcm8e8snw"
LIARA_ACCESS_KEY="t4u1cmc3n4r3hu38"
LIARA_SECRET_KEY="bb22d137-ae06-4d81-9262-5e9afc9de151"

class S3Handler():

    def __init__(self):
        self.resources = self.connect()
        self.bucket = self.resources.Bucket(LIARA_BUCKET_NAME)
    
    def connect(self):
        try:
            s3_resource = boto3.resource(
                's3',
                endpoint_url=LIARA_ENDPOINT,
                aws_access_key_id=LIARA_ACCESS_KEY,
                aws_secret_access_key=LIARA_SECRET_KEY
            )
        except Exception as exp:
            print(f'[ERROR] {exp}')
            return None
        else:
            return s3_resource

    def store(self, body, filename):
        try:
            self.bucket.put_object(
                ACL='private',
                Body=body,
                Key=filename
            )
        except ClientError as e:
            print(e)

    def download(self, filename):
        try:
            download_path = f'tmp/{filename}'
            os.makedirs('tmp', exist_ok=True)

            self.bucket.download_file(
                filename,
                download_path
            )
        except ClientError as e:
            print(e)

    def read_file(self, filename):
        self.download(filename)
        download_path = f'tmp/{filename}'
        if os.path.exists(download_path):
            text = None
            with open(download_path, 'r') as f:
                text = f.read()

            os.remove(download_path)

            return text

