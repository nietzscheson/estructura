import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import (JSON, Boolean, DateTime, ForeignKey, Integer, String,
                        Text, event)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy_state_machine import StateConfig, StateMixin

from src.enums import (AccountSubscriptionInterval, AccountSubscriptionType,
                       DocumentStatus)


def default_uuid():
    return uuid.uuid4().hex


def default_ttl():
    return datetime.now() + timedelta(days=1)


def utc_now():
    return datetime.now(timezone.utc)


def default_expiration():
    return datetime.now() + timedelta(days=30)


class Base(DeclarativeBase):
    pass


class Resource:
    id: Mapped[str] = mapped_column(
        String(32), primary_key=True, index=True, default=default_uuid
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, onupdate=utc_now, nullable=False
    )


class User(Base, Resource):
    __tablename__ = "users"

    sub: Mapped[str] = mapped_column(String, index=True)
    email: Mapped[str] = mapped_column(String, index=True)


class UserAware:
    user_id: Mapped[str] = mapped_column(
        String(32), ForeignKey("users.id"), nullable=False
    )


class Account(Base, Resource, UserAware):
    __tablename__ = "accounts"

    subscription_type: Mapped[str] = mapped_column(
        String, default=AccountSubscriptionType.FREE.value, nullable=True
    )
    subscription_interval: Mapped[str] = mapped_column(
        String, default=AccountSubscriptionInterval.MONTH.value, nullable=True
    )

    pages_limit: Mapped[int] = mapped_column(Integer, default=10)
    pages_used: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    user: Mapped["User"] = relationship("User")


class Structure(Base, Resource, UserAware):
    __tablename__ = "structures"
    __user_aware__ = True

    name: Mapped[str] = mapped_column(String, index=True, nullable=False)
    structure: Mapped[dict] = mapped_column(JSON, nullable=True)

    documents: Mapped[list["Document"]] = relationship(
        "Document", back_populates="structure"
    )


class Document(Base, Resource, UserAware, StateMixin):
    __tablename__ = "documents"
    __user_aware__ = True

    textract_job_id: Mapped[str] = mapped_column(String, index=True, nullable=True)
    textract_job_result: Mapped[dict] = mapped_column(JSON, nullable=True)
    file_storage_key: Mapped[str] = mapped_column(String, nullable=True)
    result: Mapped[dict] = mapped_column(JSON, nullable=True)
    analysis: Mapped[dict] = mapped_column(JSON, nullable=True)
    structure_id: Mapped[str] = mapped_column(
        String(32), ForeignKey("structures.id"), nullable=False
    )

    structure: Mapped["Structure"] = relationship("Structure")
    pages: Mapped[list["Page"]] = relationship("Page", back_populates="document")

    transitions = [
        {
            "trigger": "processing",
            "source": DocumentStatus.NEW.value,
            "dest": DocumentStatus.PROCESSING.value,
        },
        {
            "trigger": "completed",
            "source": DocumentStatus.PROCESSING.value,
            "dest": DocumentStatus.COMPLETED.value,
        },
        {"trigger": "fail", "source": "*", "dest": DocumentStatus.FAILED.value},
        {
            "trigger": "retry",
            "source": DocumentStatus.FAILED.value,
            "dest": DocumentStatus.PROCESSING.value,
        },
    ]

    state_config = StateConfig(
        initial=DocumentStatus.NEW.value,
        states=[status.value for status in DocumentStatus],
        transitions=transitions,
    )

    status: Mapped[str] = mapped_column(
        String, nullable=False, default=DocumentStatus.NEW.value
    )

    @property
    def file(self) -> str:
        return self.file_storage_key


class Page(Base, Resource):
    __tablename__ = "pages"

    number: Mapped[int] = mapped_column(Integer, nullable=False)
    result: Mapped[str] = mapped_column(Text, nullable=False)
    analysis: Mapped[dict] = mapped_column(JSON, nullable=True)
    document_id: Mapped[str] = mapped_column(
        String(32), ForeignKey("documents.id"), nullable=False
    )

    document: Mapped["Document"] = relationship("Document", back_populates="pages")


event.listen(Document, "init", Document.init_state_machine)
event.listen(Document, "load", Document.init_state_machine)
