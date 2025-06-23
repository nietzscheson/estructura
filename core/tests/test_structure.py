import pytest

from tests.factories import StructureFactory


@pytest.mark.asyncio
async def test_structure(db, http_client, user_aware):
    response = await http_client.get("/structures")

    assert response.status_code == 200

    data = response.json()

    assert data == []

    structure_factory = StructureFactory.build()

    params = {"name": structure_factory.name, "structure": structure_factory.structure}

    response = await http_client.post("/structures", json=params)

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == params["name"]
    assert data["structure"] == params["structure"]

    response = await http_client.get("/structures/" + data["id"])

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == params["name"]
    assert data["structure"] == params["structure"]

    params = {"name": "Banks Statements", "structure": {}}

    response = await http_client.put("/structures/" + data["id"], json=params)

    data = response.json()

    assert data["name"] == params["name"]
    assert data["structure"] == params["structure"]

    response = await http_client.delete("/structures/" + data["id"])

    data = response.json()

    assert data["message"] == "Successfully deleted"

    for x in range(0, 10):
        structure_factory = StructureFactory.build(user_id=user_aware.id)
        db.add(structure_factory)

    db.commit()

    response = await http_client.get("/structures")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 10
