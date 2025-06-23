from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: Optional[str] = Field(default="estructura")
    AWS_DEFAULT_REGION: str = Field(default="us-east-2")
    DATABASE_URL: Optional[str] = Field(
        default="postgresql://postgres:postgres@localhost:6543/postgres"
    )
    DYNAMODB_HOST: Optional[str] = Field(None)
    BUCKET_FILES_NAME: str = Field(default="estructura-default-files")
    BUCKET_SAMPLER_NAME: str = Field(default="estructura-default-samples")
    GROQ_MODEL_NAME: str = Field(default="llama-3.3-70b-versatile")
    # BEDROCK_MODEL_NAME: str = Field(default="us.anthropic.claude-3-5-haiku-20241022-v1:0")
    BEDROCK_MODEL_NAME: str = Field(
        default="us.anthropic.claude-3-5-sonnet-20241022-v2:0"
    )
    BUCKET_FILES_DOMAIN_NAME: str = Field(
        default="estructura-dev-files.s3.us-east-2.amazonaws.com",
        description="Domain name for the bucket files",
    )

    SQS_DOCUMENT_PROCESSING_URL: Optional[str] = Field(
        default="https://sqs.us-east-1.amazonaws.com/218585378150/estructura-default-document-processing",
        description="SQS queue url for Document Processing",
    )

    ALLOW_ORIGINS: list = Field(
        default=[
            "localhost:3000",
            "localhost:3001",
            "http://localhost:3000",
            "http://localhost:3001",
            "https://my.estructura.nietzscheson.com",
        ]
    )

    DEFAULT_STRUCTURE: dict = {
        "title": "Receipt",
        "description": "General Receipt",
        "type": "object",
        "required": ["key_number", "person_name"],
        "properties": {
            "key_number": {
                "type": "string",
                "description": "Unique transaction or folio number",
            },
            "person_name": {
                "type": "string",
                "description": "Name of the person or entity",
            },
            "business_name": {"type": "string", "description": "Business name"},
            "rfc": {"type": "string", "description": "RFC number"},
            "address": {"type": "string", "description": "Business address"},
            "order_number": {"type": "string", "description": "Order number"},
            "date_time": {
                "type": "string",
                "description": "Date and time of the transaction",
            },
            "items": {
                "type": "array",
                "description": "List of purchased items",
                "items": {
                    "type": "object",
                    "properties": {
                        "quantity": {
                            "type": "number",
                            "description": "Quantity of items",
                        },
                        "description": {
                            "type": "string",
                            "description": "Item description",
                        },
                        "amount": {
                            "type": "number",
                            "description": "Price per item or total for that line",
                        },
                    },
                    "required": ["quantity", "description", "amount"],
                },
            },
            "subtotal": {"type": "number", "description": "Subtotal amount"},
            "total": {"type": "number", "description": "Total amount"},
            "payment_method": {"type": "string", "description": "Payment method used"},
            "note": {
                "type": "string",
                "description": "Additional note or legend on the receipt",
            },
        },
    }


    MY_DOMAIN_NAME: str = Field(default="https://my.estructura.nietzscheson.com")


settings = Settings()
