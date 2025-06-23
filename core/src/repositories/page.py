from src.args import PageArgs
from src.models import Page
from src.repositories.base import BaseRepository
from src.schemas import PageResponse


class PageRepository(BaseRepository[Page, PageArgs, PageResponse]):
    def get_one_by_document_id_number_index(self, document_id: str, number: str):
        with self.session() as session:
            page = (
                session.query(self.model)
                .filter(
                    self.model.document_id == document_id, self.model.number == number
                )
                .first()
            )

            return page

    def get_all_by_document_id(self, document_id: str) -> list[Page]:
        with self.session() as session:
            pages = (
                session.query(self.model)
                .filter(self.model.document_id == document_id)
                .all()
            )

            return pages

    def update_analysis_by_id(self, id: str, analysis: str) -> Page:
        with self.session() as session:
            page = session.query(self.model).filter(self.model.id == id).first()

            page.analysis = analysis
            session.commit()
            session.refresh(page)

            return page
