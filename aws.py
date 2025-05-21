"""Amazon S3 Library"""
import os
import re
import sys
import threading
from dataclasses import dataclass

import boto3
import botocore

from helpers import ConfigurationHelper


class AwsS3:
    """Aws S3 Bucket"""

    def __init__(self):
        # Set up session with your AWS credentials
        self.session = boto3.Session(
            aws_access_key_id="aws_access_key_id",
            aws_secret_access_key="aws_secret_access_key",
        )

        self.services = [
            "asr_wav2vec2",
            "asr_whisper",
            "chat_gpt_turbo",
            "face_and_emotion_recognizer",
            "jobs",
            "hologram",
            "nlp_bert",
            "noise_suppression",
            "translation",
            "websocket_car_server",
            "question_answering",
        ]
        # Create a client for the S3 service
        self.s3_client = self.session.client(
            "s3",
            config=boto3.session.Config(signature_version="s3v4"),
            region_name="eu-central-1",
        )

        # AmazonS3 Bucket Name
        self.s3_bucket_name = "assistant01"
        self.assistant_version_folder = "assistant_versions"

    def upload_file(
        self,
        file_path: str,
        assistant_version: str,
        service_name: str,
        service_version: str,
    ) -> None:
        """Upload a file on the s3 bucket

        Args:
            file_path (str): file path to upload on S3 Bucket
            assistant_version (str): version of assistant
            service_name (str): name of existing service
            service_version (str): version of service
        """
        self.check_version_format_and_service_name(
            [assistant_version, service_version], service_name
        )
        if os.path.exists(file_path):
            file_name = os.path.basename(file_path)
            s3_file_path = (
                f"{self.assistant_version_folder}/"
                f"{assistant_version}/{service_name}/{service_version}/{file_name}"
            )
            # checking file is exist or not on the s3
            is_file_exist_on_s3 = self.s3_client.list_objects_v2(
                Bucket=self.s3_bucket_name, Prefix=s3_file_path
            )
            if "Contents" not in is_file_exist_on_s3:
                self.s3_client.upload_file(
                    file_path,
                    self.s3_bucket_name,
                    s3_file_path,
                    Callback=ProgressPercentage(file_path),
                )
                return
            raise FileExistsError(f"File exist on s3 | path {s3_file_path}")
        raise FileNotFoundError("File not exist.")

    def check_version_format_and_service_name(
        self, versions: list, service_name: str
    ) -> None:
        """Validate version format and checking service name

        Args:
            versions (list): version
            service_name (str): existing services name
        """
        if service_name not in self.services:
            raise RuntimeError(
                f"Wrong Service name, Available services are: {self.services}"
            )

        for version in versions:
            if not re.match(r"^(\d+)\.(\d+)\.(\d+)$", version):
                raise RuntimeError(
                    "Invalid version format, version format should be: x.y.x example: 1.1.5"
                )

    def generate_download_link(
        self,
        assistant_version: str,
        service_name: str,
        service_version: str,
        expiry_in_sec: int = 0,
    ) -> str:
        """Generate Temporary download link

        Args:
            assistant_version (str): version of assistant
            service_name (str): name of existing service
            service_version (str): version of service
            expiry_in_sec (int): link expire time in seconds

        Returns:
            str: Download Url of S3 file.
        """
        s3_file_path = (
            f"{self.assistant_version_folder}/{assistant_version}/"
            f"{service_name}/{service_version}/{service_name}"
        )

        if expiry_in_sec == 0:
            # set to seven days
            expiry_in_sec = 604800
        return self.s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.s3_bucket_name, "Key": s3_file_path},
            HttpMethod="GET",
            ExpiresIn=expiry_in_sec,
        )


@dataclass
class ProgressPercentage:
    """Show the percentage during uploading a file to the AWS S3"""

    def __init__(self, filename):
        """
        Args:
            filename: File Name
        """
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        """using for show the file uploading progress

        Args:
            bytes_amount: number of bytes
        """
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                f"\r{self._filename}  {self._seen_so_far} / {self._size}  ({percentage:.2f}%)"
            )
            sys.stdout.flush()


if __name__ == "__main__":
    try:
        for service in AwsS3().services:
            AwsS3().upload_file(
                file_path=f"/file_path/{service}",
                assistant_version="1.0.0",
                service_name=f"{service}",
                service_version="1.0.0",
            )
    except botocore.exceptions.ClientError as e:
        print(f"{e=}")
        raise
