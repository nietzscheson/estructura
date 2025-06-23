from botocore.exceptions import ClientError

from src.exceptions import UploadError


class Sampler:
    def __init__(self, bucket_name: str, s3_client):
        self.bucket_name = bucket_name
        self.s3_client = s3_client

    def __call__(self, key: str) -> bytes:
        """
        Downloads a file from an S3 bucket and returns its content as bytes.

        Args:
            key (str): The S3 object key.

        Returns:
            bytes: The file content.
        """
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=key)
            return response["Body"].read()
        except ClientError as e:
            error_message = e.response["Error"]["Message"]
            raise UploadError(f"Error al leer el archivo de S3: {error_message}") from e
        except Exception as e:
            raise UploadError(f"Ocurrió un error inesperado: {str(e)}") from e