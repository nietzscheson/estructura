from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from src.container import MainContainer
from src.repositories.account import AccountRepository
from src.schemas import AccountResponse
from src.services.current_user import current_user

main_container = MainContainer()


router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("/me")
@inject
async def me(
    account_repository: AccountRepository = Depends(
        Provide[MainContainer.account_repository]
    ),
    current_user: str = Depends(current_user),
) -> AccountResponse:
    account = account_repository.get_by_user_id(user_id=current_user.id)

    _account = AccountResponse(
        id=account.id,
        subscription_type=account.subscription_type,
        subscription_interval=account.subscription_interval,
        pages_limit=account.pages_limit,
        pages_used=account.pages_used,
    )

    return _account