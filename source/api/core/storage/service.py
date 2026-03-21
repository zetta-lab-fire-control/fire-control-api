from datetime import timedelta

from clients.minio import MinioClient


class MinioService:
    def __init__(self):
        self.client = MinioClient().client

    @property
    def buckets(self):
        return [
            "reports",
        ]

    def create_buckets(self):
        for bucket in self.buckets:
            if not self.client.bucket_exists(bucket):
                self.client.make_bucket(bucket)

    def generate_upload_url(
        self, bucket_name, object_name, expires_in_minutes: int = 15
    ):

        if bucket_name not in self.buckets:
            raise ValueError(f"Bucket '{bucket_name}' is not allowed.")

        if not self.client.bucket_exists(bucket_name):
            self.client.make_bucket(bucket_name)

        return self.client.presigned_put_object(
            bucket_name, object_name, expires=timedelta(minutes=expires_in_minutes)
        )

    def generate_download_url(
        self, bucket_name: str, object_name: str, expires_in_minutes: int = 15
    ):

        if bucket_name not in self.buckets:
            raise ValueError(f"Bucket '{bucket_name}' is not valid.")

        if not self.client.bucket_exists(bucket_name):
            raise ValueError(f"Bucket '{bucket_name}' does not exist.")

        return self.client.presigned_get_object(
            bucket_name, object_name, expires=timedelta(minutes=expires_in_minutes)
        )
