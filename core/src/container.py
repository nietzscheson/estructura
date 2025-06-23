import logging

import boto3
import httpx
from anthropic import AnthropicBedrock
from botocore.config import Config
from dependency_injector import containers, providers
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_aws import ChatBedrock
from langchain_groq import ChatGroq
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.models import (Account,  # Workspace,; WorkspaceDocumentWebhook,; Key,
                        Document, Page, Structure, User)
# from src.repositories.key import KeyRepository
from src.repositories.account import AccountRepository
from src.repositories.document import DocumentRepository
from src.repositories.page import PageRepository
from src.repositories.structure import StructureRepository
# from src.repositories.workspace import WorkspaceRepository
from src.repositories.user import UserRepository
from src.schemas import (AccountResponse, DocumentResponse, PageResponse,
                         StructureResponse, UserResponse)
from src.services.page_analysis import PageAnalysis
from src.services.queuer import Queuer
from src.services.textract import Textract
from src.services.uploader import Uploader
from src.settings import Settings
from src.services.sampler import Sampler


def configure_logging(level=logging.INFO):
    logger = logging.getLogger(__name__)
    logger.setLevel(level)

    return logger


class MainContainer(containers.DeclarativeContainer):
    settings = providers.Configuration(pydantic_settings=[Settings()])

    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.main",
            "src.routes.structures",
            "src.routes.documents",
            "src.routes.accounts",
        ]
    )

    logger = providers.Resource(
        configure_logging,
        level=logging.INFO,
    )

    engine = providers.Singleton(
        create_engine, settings.DATABASE_URL, echo=False, future=True
    )

    session_factory = providers.Singleton(
        sessionmaker,
        bind=engine,
        class_=Session,
        expire_on_commit=False,
        autoflush=False,
    )

    session = providers.Factory(session_factory)

    document = providers.Factory(Document)

    s3_client = providers.Singleton(boto3.client, "s3")

    sqs_client = providers.Singleton(boto3.client, "sqs")

    step_functions_client = providers.Singleton(boto3.client, "stepfunctions")

    cognito_client = providers.Singleton(boto3.client, "cognito-idp")

    textract_client = providers.Singleton(
        boto3.client, "textract", region_name=settings.AWS_DEFAULT_REGION
    )

    x_bedrock_client = providers.Singleton(boto3.client, "bedrock")

    bedrock_client = providers.Singleton(
        ChatBedrock,
        model_id=settings.BEDROCK_MODEL_NAME,
        model_kwargs=dict(
            top_k=250,
            top_p=0.9,
            temperature=0.1,
            max_tokens=8000,
            stop_sequences=[],
        ),
        streaming=True,
        callbacks=[StreamingStdOutCallbackHandler()],
        config=Config(
            retries=dict(max_attempts=10, mode="adaptive", total_max_attempts=100)
        ),
    )

    uploader = providers.Singleton(
        Uploader, s3_client=s3_client, bucket_name=settings.BUCKET_FILES_NAME
    )
    
    sampler = providers.Singleton(
        Sampler, s3_client=s3_client, bucket_name=settings.BUCKET_SAMPLER_NAME
    )
    
    queuer = providers.Singleton(Queuer, sqs_client=sqs_client)

    textract = providers.Singleton(
        Textract,
        client=textract_client,
    )

    user_repository = providers.Singleton(
        UserRepository,
        session=session,
        model=User,
        response=UserResponse,
    )

    account_repository = providers.Singleton(
        AccountRepository,
        session=session,
        model=Account,
        response=AccountResponse,
    )

    structure_repository = providers.Singleton(
        StructureRepository,
        session=session,
        model=Structure,
        response=StructureResponse,
    )

    document_repository = providers.Singleton(
        DocumentRepository, session=session, model=Document, response=DocumentResponse
    )

    page_repository = providers.Singleton(
        PageRepository, session=session, model=Page, response=PageResponse
    )

    antropic_bedrock = providers.Singleton(
        AnthropicBedrock,
    )

    http_client = providers.Singleton(
        httpx.Client,
    )

    groq_client = providers.Singleton(
        ChatGroq,
        model=settings.GROQ_MODEL_NAME,
        model_kwargs=dict(
            # top_k=250,
            top_p=0.9,
        ),
        temperature=0.1,
        max_tokens=8000,
        timeout=None,
        max_retries=3,
        #        stop_sequences=[],
        #        streaming=True,
        #        callbacks=[StreamingStdOutCallbackHandler()],
        #        config=Config(
        #            retries=dict(max_attempts=10, mode='adaptive', total_max_attempts=100)
        #        )
    )

    page_analysis_service = providers.Factory(
        PageAnalysis,
        groq_client=groq_client,
        logger=logger,
    )
