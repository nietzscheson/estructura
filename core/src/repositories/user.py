from typing import Optional

from src.args import UserArgs
from src.models import User
from src.repositories.base import BaseRepository
from src.schemas import UserResponse


class UserRepository(BaseRepository[User, UserArgs, UserResponse]):
    def get_by_sub(self, sub: str) -> Optional[User]:
        with self.session() as session:
            return session.query(self.model).filter_by(sub=sub).first()
