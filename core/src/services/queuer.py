import json

from botocore.exceptions import ClientError

from src.exceptions import UploadError


class Queuer:
    def __init__(self, sqs_client):
        self.sqs_client = sqs_client

    def __call__(self, message: object, sqs_url: str):
        try:
            response = self.sqs_client.send_message(
                QueueUrl=sqs_url, MessageBody=json.dumps(message)
            )

            return response
        except ClientError as e:
            error_message = e.response["Error"]["Message"]
            raise UploadError(f"Error al subir el archivo a S3: {error_message}") from e
        except Exception as e:
            raise UploadError(f"Ocurrió un error inesperado: {str(e)}") from e
