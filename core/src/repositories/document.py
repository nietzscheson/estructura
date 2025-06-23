from src.args import DocumentArgs
from src.models import Document
from src.repositories.base import BaseRepository
from src.schemas import DocumentResponse


class DocumentRepository(BaseRepository[Document, DocumentArgs, DocumentResponse]):
    def get_one_by_user_id(self, user_id: str):
        with self.session() as session:
            instance = (
                session.query(self.model).filter(self.model.user_id == user_id).first()
            )
            return instance

    def get_one_by_textract_job_id(self, textract_job_id: str) -> Document:
        with self.session() as session:
            instance = (
                session.query(self.model)
                .filter(self.model.textract_job_id == textract_job_id)
                .first()
            )
            return instance

    #
    def update_textract_job_result_by_id(
        self, document_id: str, textract_job_result: str
    ) -> Document:
        with self.session() as session:
            instance = (
                session.query(self.model).filter(self.model.id == document_id).first()
            )

            instance.textract_job_result = textract_job_result

            session.add(instance)
            session.commit()

            session.refresh(instance)

            return instance
