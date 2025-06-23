import os

from dependency_injector.wiring import Provide, inject
from fastapi import (APIRouter, Depends, File, Form, HTTPException, Response,
                     UploadFile, status)

from src.args import DocumentArgs
from src.container import MainContainer
from src.repositories.account import AccountRepository
from src.repositories.document import DocumentRepository
from src.repositories.page import PageRepository
from src.schemas import DocumentResponse, PageResponse, QueryParamsScheme
from src.services.current_user import current_user
from src.services.queuer import Queuer
from src.services.uploader import Uploader
from src.settings import settings

main_container = MainContainer()


router = APIRouter(prefix="/documents", tags=["documents"])


@router.get("")
@inject
async def all(
    response: Response,
    params: QueryParamsScheme = Depends(),
    repository: DocumentRepository = Depends(
        Provide[MainContainer.document_repository]
    ),
    current_user: str = Depends(current_user),
):
    result = repository.all(params=params, user_id=current_user.id)

    response.headers["Content-Range"] = f"{params.range}/{result.total}"

    return result.items


@router.post("")
@inject
async def create(
    file: UploadFile = File(...),
    structure_id: str = Form(...),
    repository: DocumentRepository = Depends(
        Provide[MainContainer.document_repository]
    ),
    uploader: Uploader = Depends(Provide[MainContainer.uploader]),
    queuer: Queuer = Depends(Provide[MainContainer.queuer]),
    current_user: str = Depends(current_user),
    account_repository: AccountRepository = Depends(
        Provide(MainContainer.account_repository)
    ),
) -> DocumentResponse:
    try:
        account = account_repository.get_by_user_id(user_id=current_user.id)

        if not account or not account.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Inactive account"
            )

        if account.pages_used >= account.pages_limit:
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail="Page limit reached. Upgrade your plan to continue.",
            )

        content = await file.read()
        content_type = file.content_type
        extension = os.path.splitext(file.filename)[1]

        s3_key = uploader(
            content=content, content_type=content_type, extension=extension
        )

        document_create_args = DocumentArgs(
            # textract_job_id=textract_job_id,
            file_storage_key=s3_key,
            structure_id=structure_id,
        )

        document = repository.create(args=document_create_args, user_id=current_user.id)

        message = {"document_id": document.id}
        queuer(message=message, sqs_url=settings.SQS_DOCUMENT_PROCESSING_URL)
        document.processing()

        repository.persist(instance=document)

        response_model = DocumentResponse(
            id=str(document.id),
            file=f"https://{settings.BUCKET_FILES_DOMAIN_NAME}/{document.file_storage_key}",
            pages=[],
            structure_id=document.structure_id,
            created_at=document.created_at,
            status=document.status,
        )

        return response_model
    except Exception as e:
        print(e)
        raise e


@router.get("/{id}")
@inject
async def one(
    id: str,
    document_repository: DocumentRepository = Depends(
        Provide[MainContainer.document_repository]
    ),
    pages_repository: PageRepository = Depends(Provide[MainContainer.page_repository]),
    current_user: str = Depends(current_user),
) -> DocumentResponse:
    document = document_repository.one(id=id, user_id=current_user.id)

    pages = pages_repository.get_all_by_document_id(document_id=document.id)

    _pages = []

    for page in pages:
        _pages.append(
            PageResponse(id=page.id, number=page.number, analysis=page.analysis)
        )

    _document = DocumentResponse(
        id=document.id,
        file=f"https://{settings.BUCKET_FILES_DOMAIN_NAME}/{document.file_storage_key}",
        # created_at=document.created_at,
        # job_id=document.textract_job_id,
        pages=_pages,
        structure_id=document.structure_id,
        created_at=document.created_at,
        status=document.status,
    )

    return _document
