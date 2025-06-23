import json
from typing import Generic, List, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlmodel import SQLModel

from src.schemas import QueryParamsScheme

Model = TypeVar("Model", bound=SQLModel)
Args = TypeVar("Args", bound=BaseModel)
Response = TypeVar("Response", bound=BaseModel)


class PaginatedResult(SQLModel, Generic[Response]):
    items: List[Response]
    total: int
    start: int
    end: int


class BaseRepository(Generic[Model, Args, Response]):
    def __init__(
        self, session: AsyncSession, model: Type[Model], response: Type[Response]
    ):
        self.session = session
        self.model = model
        self.response = response

    def all(
        self, params: QueryParamsScheme, user_id: str = None
    ) -> PaginatedResult[Model]:
        start, end = json.loads(params.range)
        sort_attribute, sort_direction = json.loads(params.sort)

        order_by = getattr(self.model, sort_attribute)
        if sort_direction.lower() == "desc":
            order_by = order_by.desc()

        with self.session() as session:
            query = session.query(self.model).order_by(order_by)

            filters = json.loads(params.filter or "{}")

            if getattr(self.model, "__user_aware__", False) and user_id:
                query = query.filter(self.model.user_id == user_id)

            if filters:
                query.filter_by(**filters)

            total_count = query.count()

            items = query.offset(start).limit((end - start) + 1).all()

            return PaginatedResult(
                items=[self.response.model_validate(item) for item in items],
                total=total_count,
                start=start,
                end=end,
            )

    def create(self, args: Args, user_id: str = None) -> Model:
        with self.session() as session:
            data = args.model_dump()

            if getattr(self.model, "__user_aware__", False) and user_id:
                data["user_id"] = user_id

            instance = self.model(**data)

            session.add(instance)
            session.commit()
            session.refresh(instance)

            # response = self.response.model_validate(instance, from_attributes=True)

            return instance

    def one(self, id: str, user_id: str = None, session: Session = None) -> Model:
        if session:
            return self._one(id=id, user_id=user_id, session=session)

        with self.session() as session:
            return self._one(id=id, user_id=user_id, session=session)

    def _one(self, id: str, user_id: str, session: Session) -> Model:
        query = session.query(self.model).filter(self.model.id == id)

        if getattr(self.model, "__user_aware__", False) and user_id:
            query = query.filter(self.model.user_id == user_id)

        return query.first()

    def update(self, id: str, args: Args, user_id: str = None) -> Model:
        with self.session() as session:
            # instance = session.query(self.model).filter(self.model.id == id).first()
            instance = self.one(id=id, user_id=user_id, session=session)

            for var, value in vars(args).items():
                setattr(instance, var, value)

            session.commit()
            session.refresh(instance)

            # response = self.response.model_validate(instance)

            return instance

    def delete(self, id: str, user_id: str = None):
        with self.session() as session:
            instance = self.one(id=id, user_id=user_id, session=session)

            session.delete(instance)
            session.commit()

            return {"message": "Successfully deleted"}

    def persist(self, instance: Model) -> Model:
        with self.session() as session:
            session.add(instance)
            session.commit()
            session.refresh(instance)
            return instance
