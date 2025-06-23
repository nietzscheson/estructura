from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.args import ProductArgs
from src.exceptions import ProductNotFoundException
from src.models import Product


class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    def create(self, args: ProductArgs):
        with self.session() as session:
            product = Product(**args.model_dump())

            session.add(product)
            session.commit()
            session.refresh(product)

            return product

    def one(self, id: str) -> Product:
        with self.session() as session:
            result = session.execute(select(Product).where(Product.id == id))
            product = result.scalars().first()

            if product is None:
                raise ProductNotFoundException(f"Product {id} not found")

            return product
