from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Response

from src.args import StructureArgs
from src.container import MainContainer
from src.repositories.structure import StructureRepository
from src.schemas import QueryParamsScheme, StructureResponse
from src.services.current_user import current_user

router = APIRouter(prefix="/structures", tags=["Structures"])


@router.get("")
@inject
async def all(
    response: Response,
    params: QueryParamsScheme = Depends(),
    repository: StructureRepository = Depends(
        Provide[MainContainer.structure_repository]
    ),
    current_user: str = Depends(current_user),
) -> list[StructureResponse]:
    result = repository.all(params=params, user_id=current_user.id)

    response.headers["Content-Range"] = f"{params.range}/{result.total}"

    return result.items


@router.post("")
@inject
async def create(
    args: StructureArgs,
    repository: StructureRepository = Depends(
        Provide[MainContainer.structure_repository]
    ),
    current_user: str = Depends(current_user),
) -> StructureResponse:
    return repository.create(args=args, user_id=current_user.id)


@router.get("/{id}")
@inject
async def one(
    id: str,
    repository: StructureRepository = Depends(
        Provide[MainContainer.structure_repository]
    ),
    current_user: str = Depends(current_user),
) -> StructureResponse:
    return repository.one(id=id, user_id=current_user.id)


@router.put("/{id}")
@inject
async def update(
    id: str,
    args: StructureArgs,
    repository: StructureRepository = Depends(
        Provide[MainContainer.structure_repository]
    ),
    current_user: str = Depends(current_user),
) -> StructureResponse:
    return repository.update(id=id, args=args, user_id=current_user.id)


@router.delete("/{id}")
@inject
async def delete(
    id: str,
    repository: StructureRepository = Depends(
        Provide[MainContainer.structure_repository]
    ),
    current_user: str = Depends(current_user),
):
    return repository.delete(id=id, user_id=current_user.id)
