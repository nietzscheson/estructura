import uuid
from datetime import datetime
from typing import List, Optional

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field, field_serializer


class QueryParamsScheme(BaseModel):
    filter: Optional[str] = "{}"
    range: Optional[str] = "[0,9]"
    sort: str = Query('["id", "ASC"]')


class ResourceResponse(BaseModel):
    id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("created_at")
    def serialize_created_at(self, value: datetime) -> str:
        return value.strftime("%Y-%m-%d %H:%M:%S")


class PageResponse(BaseModel):
    id: str
    number: int
    analysis: object = Field(None)
    model_config = ConfigDict(from_attributes=True)


class DocumentResponse(ResourceResponse):
    id: str
    pages: List[PageResponse] = Field(..., description="Pages Summary")
    file: str = Field(..., description="File Path")

    model_config = ConfigDict(from_attributes=True)
    structure_id: str = Field(..., description="Workspace ID")
    status: str = Field(..., description="Document Status")


class Page(BaseModel):
    page: int
    content: str


class Document(BaseModel):
    pages: List[Page]


class UserResponse(BaseModel):
    id: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class StructureResponse(ResourceResponse):
    id: str
    name: str
    structure: dict

    model_config = ConfigDict(from_attributes=True)


class AccountResponse(BaseModel):
    id: str
    subscription_type: Optional[str]
    subscription_interval: Optional[str]
    pages_limit: int
    pages_used: int

    model_config = ConfigDict(from_attributes=True)


class AccountSubscriptionResponse(BaseModel):
    url: str
