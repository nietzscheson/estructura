from src.args import (AccountArgs, DocumentArgs, PageArgs, StructureArgs,
                      UserArgs)
from src.container import MainContainer
from src.enums import DocumentStatus

container = MainContainer()

settings = container.settings()
user_repository = container.user_repository()
account_repository = container.account_repository()
structure_repository = container.structure_repository()
sampler = container.sampler()
uploader = container.uploader()
document_repository = container.document_repository()
page_repository = container.page_repository()


def handler(event, context):
    user_attributes = event["request"]["userAttributes"]
    email = user_attributes.get("email")
    sub = user_attributes.get("sub")

    if not email or not sub:
        raise Exception("Missing email or sub.")

    user = user_repository.get_by_sub(sub=sub)

    if not user:
        user_args = UserArgs(email=email, sub=sub)
        user = user_repository.create(args=user_args)

    account = account_repository.get_by_user_id(user_id=user.id)

    if not account:
        account_args = AccountArgs(user_id=user.id)
        account_repository.create(args=account_args)

    # Crear Structure

    structure = structure_repository.get_by_user_id(user_id=user.id)

    if not structure:
        structure_args = StructureArgs(
            name="Receipt",
            structure=settings["DEFAULT_STRUCTURE"],
        )
        structure = structure_repository.create(args=structure_args, user_id=user.id)

    sampler_object = sampler(key="receipts/receipt_2.jpeg")

    document_key = uploader(
        content=sampler_object, content_type="image/jpeg", extension=".jpeg"
    )

    document = document_repository.get_one_by_user_id(user_id=user.id)

    if not document:
        document_args = DocumentArgs(
            textract_job_id="",
            file_storage_key=document_key,
            structure_id=structure.id,
        )

        document = document_repository.create(args=document_args, user_id=user.id)

    if document.status == DocumentStatus.NEW.value:
        document.processing()

        document_repository.persist(instance=document)

    if document.status == DocumentStatus.PROCESSING.value:
        document.completed()

        document_repository.persist(instance=document)

    page = page_repository.get_one_by_document_id_number_index(
        document_id=document.id, number=1
    )

    if not page:
        result = "EL PIBITO FRANCISCO JOSE RODRIGUEZ INTERIAN RFC:ROIF670220E45 AV 135 M 72 L45 SM 321 CANCUN QUINTANA ROO MEXIC 0 CP 77560 LUGAR DE EXPEDICION FOLIO:27060 ORDEN:6 FECHA: 19/03/2025 08:50:46 AM CAJERO:CAJER@ CANT. DESCRIPCION IMPORTE 2 TORTA COCHINITA $100.00 SUBTOTAL: $100.00 TOTAL: $100.00 SON:CIEN PESOS 00/100 M.N. FORMAS DE PAGO CREDITO: $100.00 ESTE NO ES UN COMPROBANTE FISCAL ***SOFT RESTAURANT V10 ***"
        page_args = PageArgs(
            document_id=document.id,
            result=result,
            number=1,
        )

        page = page_repository.create(args=page_args)

        analysis = {
            "address": "AV 135 M 72 L45 SM 321 CANCUN QUINTANA ROO MEXIC",
            "business_name": "EL PIBITO",
            "date_time": "2025-03-19T08:50:46",
            "items": [
                {"amount": 100.0, "description": "TORTA COCHINITA", "quantity": 2}
            ],
            "key_number": "27060",
            "note": "ESTE NO ES UN COMPROBANTE FISCAL",
            "order_number": "6",
            "payment_method": "CREDITO",
            "person_name": "FRANCISCO JOSE RODRIGUEZ INTERIAN",
            "rfc": "ROIF670220E45",
            "subtotal": 100.0,
            "total": 100.0,
        }

        page_repository.update_analysis_by_id(id=page.id, analysis=analysis)

    return event
