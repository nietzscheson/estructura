from typing import Optional

from pydantic import BaseModel, Field

from src.enums import AccountSubscriptionInterval, AccountSubscriptionType


class DocumentArgs(BaseModel):
    textract_job_id: Optional[str] = Field(None, description="Textract Job ID")
    file_storage_key: Optional[str] = Field(None, description="Storage key of the file")
    structure_id: Optional[str] = Field(None, description="Structure ID")


class StructureArgs(BaseModel):
    name: str = Field(..., description="Structure Name")
    structure: dict = Field(..., description="Structure Object")


class UserArgs(BaseModel):
    email: str = Field(..., description="User email")
    sub: str = Field(..., description="Cognito sub")


class AccountArgs(BaseModel):
    user_id: str = Field(..., description="User ID")


class SubscriptionArgs(BaseModel):
    account_id: str = Field(..., description="Account ID")


class WorkspaceArgs(BaseModel):
    name: str = Field(..., description="Workspace Name")
    webhook: Optional[str] = Field(default=None, description="Workspace Webhook URL")
    structure_id: str = Field(..., description="Structure ID")


class WorkspaceDocumentWebhookArgs(BaseModel):
    document_id: str = Field(..., description="Document ID")
    status_code: str = Field(..., description="Status Code")
    response: str = Field(..., description="Status Message")


class KeyArgs(BaseModel):
    name: str = Field(..., description="Key")
    expires: bool = Field(default=False)
    expires_at: Optional[str] = Field(None, description="Key Expiration")


class BlockCreateArgs(BaseModel):
    name: str = Field(..., description="Template Name")
    structure_id: str = Field(..., description="Template ID")
    block: dict = Field(..., description="Block")


class PageArgs(BaseModel):
    document_id: str = Field(..., description="Document ID")
    result: str = Field(None, description="Textract Page Result")
    number: int = Field(None, description="Number of the Page")


class AccountSubscriptionArgs(BaseModel):
    type: AccountSubscriptionType = Field(default=AccountSubscriptionType.FREE.value)
    interval: AccountSubscriptionInterval = Field(
        default=AccountSubscriptionInterval.MONTH.value
    )
