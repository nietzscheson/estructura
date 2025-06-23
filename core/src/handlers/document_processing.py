import json
import logging

from src.args import PageArgs
from src.container import MainContainer
from src.services.exception_handler import ExceptionHandler


logger = logging.getLogger()
logger.setLevel("INFO")


def page_analysis(page_id: str, structure: dict, account_id: str):
    logger.info(f"Page ID: {page_id}")

    main_container = MainContainer()
    page_repository = main_container.page_repository()
    page_analysis_service = main_container.page_analysis_service()
    account_repository = main_container.account_repository()

    try:
        page = page_repository.one(id=page_id)

        logger.info(f"Page: {page.number} | {page.id}")

        analysis = page_analysis_service(
            page_content=page.result, page_number=page.number, structure=structure
        )

        logger.info(f"Analysis: {analysis}")

        page_repository.update_analysis_by_id(id=page_id, analysis=analysis)

        account_repository.page_used(id=account_id)

        return page.id
    except Exception as e:
        exception_handler = ExceptionHandler()
        return exception_handler(e)


def handler(
    event,
    context,
):
    main_container = MainContainer()
    textract = main_container.textract()
    uploader = main_container.uploader()
    document_repository = main_container.document_repository()
    page_analysis_service = main_container.page_analysis_service()
    page_repository = main_container.page_repository()
    structure_repository = main_container.structure_repository()
    account_repository = main_container.account_repository()

    record = event.get("Records", [])[0]

    body = json.loads(record.get("body", "{}"))

    document_id = body.get("document_id")

    logger.info(f"Document ID: {document_id}")

    document = document_repository.one(id=document_id)

    if not document:
        raise Exception(f"Document not found for id: {document_id}")

    structure = structure_repository.one(id=document.structure_id)

    if not structure:
        raise Exception(f"Structure not found for id: {document.structure_id}")

    page = page_repository.get_one_by_document_id_number_index(
        document_id=document.id, number=1
    )

    if not page:
        file_response = uploader.get(id=document.file_storage_key)

        text_detection_response = textract.text_detection(
            image=file_response,
        )
        
        page_args = PageArgs(
            document_id=document.id,
            number=1,
            result=text_detection_response,
        )

        page = page_repository.create(args=page_args)

    page_analysis = page.analysis

    if not page_analysis:
        page_analysis_response = page_analysis_service(
            page_content=page.result,
            page_number=1,
            structure=structure.structure,
        )

        page_repository.update_analysis_by_id(
            id=page.id, analysis=page_analysis_response
        )

    account = account_repository.get_by_user_id(user_id=document.user_id)

    account_repository.page_used(id=account.id)
    document.completed()
    document_repository.persist(instance=document)
    return {"document_id": document.id}