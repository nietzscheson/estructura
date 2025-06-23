import uuid

from botocore.exceptions import ClientError

from src.exceptions import UploadError


class Uploader:
    def __init__(self, bucket_name: str, s3_client):
        self.bucket_name = bucket_name
        self.s3_client = s3_client

    def __call__(
        self,
        content: bytes,
        content_type: str = "application/pdf",
        extension: str = "pdf",
    ):
        """
        Uploads a PDF file to an S3 bucket.

        Args:
            content (bytes): The PDF file content as bytes.
        """

        key = f"{uuid.uuid4().hex}{extension}"

        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name, Key=key, Body=content, ContentType=content_type
            )

            return key
        except ClientError as e:
            error_message = e.response["Error"]["Message"]
            raise UploadError(f"Error al subir el archivo a S3: {error_message}") from e
        except Exception as e:
            raise UploadError(f"Ocurrió un error inesperado: {str(e)}") from e

    def get(self, id: str):
        """
        Retrieves a PDF file from an S3 bucket.

        Args:
            key (str): The S3 object key (path and filename).
        """
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=id)
            print(response["Body"].read())
            return response["Body"].read()

        except ClientError as e:
            error_message = e.response["Error"]["Message"]
            raise UploadError(f"Error al subir el archivo a S3: {error_message}") from e
        except Exception as e:
            raise UploadError(f"Ocurrió un error inesperado: {str(e)}") from e
