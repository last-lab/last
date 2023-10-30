import os
from typing import Callable, List, Optional

import aiofiles
from starlette.datastructures import UploadFile

from last.services.exceptions import FileExtNotAllowed, FileMaxSizeLimit


class FileUpload:
    def __init__(
        self,
        uploads_dir: str,
        allow_extensions: Optional[List[str]] = None,
        max_size: int = 1024**3,
        filename_generator: Optional[Callable] = None,
        prefix: str = "/static/uploads",
    ):
        self.max_size = max_size
        self.allow_extensions = allow_extensions
        self.uploads_dir = uploads_dir
        self.filename_generator = filename_generator
        self.prefix = prefix

    async def save_file(self, filename: str, content: bytes):
        file = os.path.join(self.uploads_dir, filename)
        async with aiofiles.open(file, "wb") as f:
            await f.write(content)
        return os.path.join(self.prefix, filename)

    async def upload(self, file: UploadFile):
        if self.filename_generator:
            filename = self.filename_generator(file)
        else:
            filename = file.filename
        content = await file.read()
        file_size = len(content)
        if file_size > self.max_size:
            raise FileMaxSizeLimit(
                f"File size {file_size} exceeds max size {self.max_size}"
            )
        if self.allow_extensions:
            for ext in self.allow_extensions:
                if filename.endswith(ext):
                    raise FileExtNotAllowed(
                        f"File ext {ext} is not allowed of {self.allow_extensions}"
                    )
        return await self.save_file(filename, content)


class ALiYunOSS(FileUpload):
    """
    File upload for aliyun oss
    """

    def __init__(
        self,
        access_key: str,
        access_key_secret: str,
        bucket: str,
        endpoint: str,
        uploads_dir: str,
        allow_extensions: Optional[List[str]] = None,
        max_size: int = 1024**3,
        filename_generator: Optional[Callable] = None,
    ):
        import asyncoss

        super().__init__(uploads_dir, allow_extensions, max_size, filename_generator)
        auth = asyncoss.Auth(access_key, access_key_secret)
        self.endpoint = endpoint
        self.bucket = bucket
        self.client = asyncoss.Bucket(auth, endpoint, bucket)

    async def save_file(self, filename: str, content: bytes):
        file = os.path.join(self.uploads_dir, filename)
        async with self.client as bucket:
            await bucket.put_object(file, content)
        return f"{self.bucket}.{self.endpoint}/{file}"


class AwsS3(FileUpload):
    """
    File upload for AWS S3
    """

    def __init__(
        self,
        access_key: str,
        access_key_secret: str,
        region_name: str,
        bucket: str,
        endpoint: str,
        uploads_dir: str,
        allow_extensions: Optional[List[str]] = None,
        max_size: int = 1024**3,
        filename_generator: Optional[Callable] = None,
    ):
        import aiobotocore

        super().__init__(uploads_dir, allow_extensions, max_size, filename_generator)
        session = aiobotocore.get_session()
        self.client = session.create_client(
            "s3",
            region_name=region_name,
            aws_secret_access_key=access_key_secret,
            aws_access_key_id=access_key,
            endpoint_url=endpoint,
        )
        self.bucket = bucket
        self.endpoint = endpoint

    async def save_file(self, filename: str, content: bytes):
        file = os.path.join(self.uploads_dir, filename)
        async with self.client as client:
            await client.put_object(Bucket=self.bucket, Key=file, Body=content)
        return f"{self.bucket}.{self.endpoint}/{file}"
