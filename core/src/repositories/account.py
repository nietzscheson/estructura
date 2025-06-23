from src.args import AccountArgs
from src.models import Account
from src.repositories.base import BaseRepository
from src.schemas import AccountResponse


class AccountRepository(BaseRepository[Account, AccountArgs, AccountResponse]):
    def get_by_user_id(self, user_id: str) -> Account:
        with self.session() as session:
            return session.query(self.model).filter_by(user_id=user_id).first()

    def page_used(self, id: str):
        with self.session() as session:
            account = session.query(self.model).filter_by(id=id).first()

            if not account:
                raise ValueError(f"Account with id={id} not found")

            account.pages_used += 1
            session.add(account)
            session.commit()

            session.refresh(account)

            return account

    def update_stripe_customer_id(self, id: str, stripe_customer_id: str):
        with self.session() as session:
            account = session.query(self.model).filter_by(id=id).first()

            if not account:
                raise ValueError(f"Account with id={id} not found")

            account.stripe_customer_id = stripe_customer_id
            session.add(account)
            session.commit()

            session.refresh(account)

            return account

    def update_checkout_session_id(self, id: str, checkout_session_id: str):
        with self.session() as session:
            account = session.query(self.model).filter_by(id=id).first()

            if not account:
                raise ValueError(f"Account with id={id} not found")

            account.checkout_session_id = checkout_session_id
            session.add(account)
            session.commit()
            session.refresh(account)
            return account

    def get_by_stripe_customer_id(self, stripe_customer_id: str) -> Account:
        with self.session() as session:
            return (
                session.query(self.model)
                .filter_by(stripe_customer_id=stripe_customer_id)
                .first()
            )
