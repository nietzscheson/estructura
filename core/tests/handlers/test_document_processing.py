import json
import pytest


from src.args import DocumentArgs
from src.enums import DocumentStatus
from src.handlers.document_processing import (
    handler as document_processing_handler,
)
from tests.factories import StructureFactory, AccountFactory


def test_document_processing_handler(
    main_container,
    db,
    user_aware,
    default_structure,
    textract_event_expected_response,
    mock_textract_text_detection,
    mock_s3_get
):
    account_factory = AccountFactory.build(user_id=user_aware.id)
    db.add(account_factory)
    db.commit()

    document_repository = main_container.document_repository()

    records = textract_event_expected_response.get("Records")[0]
    body = json.loads(records.get("body"))
    message = json.loads(body.get("Message"))

    structure_factory = StructureFactory.build(
        user_id=user_aware.id, structure=default_structure
    )

    db.add(structure_factory)
    db.commit()

    document_create_args = DocumentArgs(
        textract_job_id=message.get("JobId"),
        file_storage_key="017164524d7244cbb75a2dea52394764.jpeg",
        structure_id=structure_factory.id,
    )

    document = document_repository.create(
        args=document_create_args, user_id=user_aware.id
    )
    document.processing()
    document_repository.persist(instance=document)

    event = {"Records": [{"body": json.dumps({"document_id": document.id})}]}

    document_text_detection_handler_response = document_processing_handler(event, None)

    document = document_repository.one(
        id=document_text_detection_handler_response["document_id"],
        user_id=user_aware.id,
    )

    assert document.status == DocumentStatus.COMPLETED.value
