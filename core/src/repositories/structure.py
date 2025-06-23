from src.args import StructureArgs
from src.models import Structure
from src.repositories.base import BaseRepository
from src.schemas import StructureResponse


class StructureRepository(BaseRepository[Structure, StructureArgs, StructureResponse]):
    def get_by_user_id(self, user_id: str) -> Structure:
        with self.session() as session:
            return session.query(self.model).filter_by(user_id=user_id).first()
