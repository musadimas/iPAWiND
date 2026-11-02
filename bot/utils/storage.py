import json
import logging
import mimetypes
import time
from io import BytesIO
import aioboto3
from botocore.config import Config
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

class S3Storage:
    """
    S3-compatible storage connection (RustFS, MinIO, Cloudflare R2, AWS S3)
    :param endpoint_url: S3 API endpoint url
    :type endpoint_url: string
    :param key_id: Access key id
    :type key_id: string
    :param access_key: Secret access key
    :type access_key: string
    :param bucket: Bucket name
    :type bucket: string
    :param bucket_url: Public url of the bucket, uploaded keys are appended to it
    :type bucket_url: string
    :param region: Bucket region, RustFS/MinIO accept us-east-1
    :type region: string
    """

    def __init__(self, endpoint_url, key_id, access_key, bucket, bucket_url, region="us-east-1"):
        self.session = aioboto3.Session(key_id, access_key, region_name=region)
        self.endpoint_url = endpoint_url
        self.bucket = bucket
        self.bucket_url = bucket_url.rstrip('/')
        # Self-hosted servers don't have per-bucket DNS, so use http://host/bucket/key
        self.config = Config(signature_version='s3v4', s3={'addressing_style': 'path'})

    def _client(self):
        return self.session.client('s3', endpoint_url=self.endpoint_url, config=self.config)

    async def ensure_bucket(self):
        """
        Create the bucket if missing and allow anonymous reads,
        iOS fetches the manifest and ipa without credentials
        """
        async with self._client() as client:
            try:
                await client.head_bucket(Bucket=self.bucket)
            except ClientError:
                await client.create_bucket(Bucket=self.bucket)
                logger.info(f"Created bucket {self.bucket}")

            policy = {
                "Version": "2012-10-17",
                "Statement": [{
                    "Effect": "Allow",
                    "Principal": {"AWS": ["*"]},
                    "Action": ["s3:GetObject"],
                    "Resource": [f"arn:aws:s3:::{self.bucket}/*"],
                }],
            }
            await client.put_bucket_policy(Bucket=self.bucket, Policy=json.dumps(policy))

    async def upload_file(self, file, path):
        content_type = mimetypes.guess_type(path)[0] or 'application/octet-stream'
        async with self._client() as client:
            start = time.perf_counter()
            if isinstance(file, str):
                # If the file is a string path, open the file and read it into a BytesIO object
                with open(file, 'rb') as f:
                    file_obj = BytesIO(f.read())
                await client.put_object(Bucket=self.bucket, Key=path, Body=file_obj, ContentType=content_type)
            else:
                # If file is already a file-like object, upload directly
                await client.put_object(Bucket=self.bucket, Key=path, Body=file, ContentType=content_type)
            end = time.perf_counter()
            logger.info(f"Uploaded file in {end - start:.2f} seconds.")
        return self.bucket_url + '/' + path
