from fastapi import Depends

from src.container import MainContainer
from src.models import User
from src.services.current_cognito_claims import current_cognito_claims


async def current_user(current_claims: dict = Depends(current_cognito_claims)) -> User:
    main_container = MainContainer()
    session = main_container.session()

    with session() as session:
        email = current_claims["email"]
        sub = current_claims["sub"]

        user = session.query(User).filter(User.sub == sub).first()

        if user is None:
            user = User(sub=sub, email=email)
            session.add(user)
            session.commit()

        return user
