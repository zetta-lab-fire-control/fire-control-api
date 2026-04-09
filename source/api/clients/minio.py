import os

import urllib3
from minio import Minio

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class MinioClient:
    def __init__(self):
        self.endpoint = os.getenv("MINIO_URL")
        self.access_key = os.getenv("MINIO_ROOT_USER")
        self.secret_key = os.getenv("MINIO_ROOT_PASSWORD")

    @property
    def client(self, secure=False):

        return Minio(
            self.endpoint,
            access_key=self.access_key,
            secret_key=self.secret_key,
            secure=secure,
            http_client=self.http_client,
        )

    @property
    def http_client(self):

        return urllib3.PoolManager(
            cert_reqs="CERT_NONE", retries=urllib3.Retry(total=3)
        )
