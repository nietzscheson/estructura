import uuid

import pytest

from tests.factories import StructureFactory, AccountFactory
from src.args import PageArgs
from src.enums import DocumentStatus


@pytest.mark.asyncio
async def test_document(
    http_client,
    receipts_files,
    mock_s3_uploader,
    #mock_textract_start,
    db,
    main_container,
    user_aware,
    mock_queuer,
):
    response = await http_client.get("/documents")

    assert response.status_code == 200

    data = response.json()

    assert data == []

    receipt = next(iter(receipts_files))

    file_content = receipt

    file_name = f"{uuid.uuid4}.pdf"

    files = {"file": (file_name, file_content)}

    account_factory = AccountFactory.build(user_id=user_aware.id)

    db.add(account_factory)
    db.commit()

    structure_factory = StructureFactory.build(user_id=user_aware.id)

    db.add(structure_factory)
    db.commit()

    response = await http_client.post(
        "/documents", files=files, data={"structure_id": structure_factory.id}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] is not None
    assert data["structure_id"] == structure_factory.id
    assert data["status"] == DocumentStatus.PROCESSING.value

    id = data["id"]

    page_repository = main_container.page_repository()

    page_args = PageArgs(
        document_id=id,
        number=1,
        result="EL PIBITO FRANCISCO JOSE RODRIGUEZ INTERIAN RFC:ROIF670220E45 AV 135 M 72 L45 SM 321 CANCUN QUINTANA ROO MEXIC 0 CP 77560 LUGAR DE EXPEDICION FOLIO:27060 ORDEN:6 FECHA: 19/03/2025 08:50:46 AM CAJERO:CAJER@ CANT. DESCRIPCION IMPORTE 2 TORTA COCHINITA $100.00 SUBTOTAL: $100.00 TOTAL: $100.00 SON:CIEN PESOS 00/100 M.N. FORMAS DE PAGO CREDITO: $100.00 ESTE NO ES UN COMPROBANTE FISCAL ***SOFT RESTAURANT V10 ***",
    )

    page = page_repository.create(page_args)

    page_repository.update_analysis_by_id(
        id=page.id,
        analysis={
            "business_name": "EL PIBITO",
            "address": "AV 135 M 72 L45 SM 321 CANCUN QUINTANA ROO MEXIC",
            "date_time": "2025-03-19T08:50:46",
            "items": [{"quantity": 2, "description": "TORTA COCHINITA", "amount": 100}],
            "key_number": "27060",
            "person_name": "FRANCISCO JOSE RODRIGUEZ INTERIAN",
            "rfc": "ROIF670220E45",
            "subtotal": 100,
            "total": 100,
            "order_number": "6",
            "payment_method": "CREDITO",
        },
    )

    page = page_repository.one(page.id)

    response = await http_client.get(f"/documents/{id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == id
    assert len(data["pages"]) == 1

    _page = data["pages"][0]

    assert _page["id"] == page.id
    assert _page["analysis"] == page.analysis
