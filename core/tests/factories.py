import factory

from src.models import Structure, User, Account


class UserFactory(factory.Factory):
    class Meta:
        model = User

    sub = factory.Faker("uuid4")
    email = factory.Faker("email")


class StructureFactory(factory.Factory):
    class Meta:
        model = Structure

    name = factory.Faker("name")
    structure = {
        "title": "BankStatement",
        "description": "Financial specialist parsing a bank statement. Extract and structure transaction data, ignoring summaries or non-transactional lines.",
        "type": "object",
        "required": [],
        "properties": {
            "account_number": {"type": "string", "description": "Account number"},
            "bank_name": {"type": "string", "description": "Bank name"},
            "customer_name": {"type": "string", "description": "Customer name"},
            "statement_date": {"type": "string", "description": "Statement date"},
            "transactions": {
                "type": "array",
                "description": "List of bank statement transactions",
                "items": {"$ref": "#/definitions/BankStatementTransaction"},
            },
        },
        "definitions": {
            "BankStatementTransaction": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "Transaction ID/Reference or Folio",
                    },
                    "date": {"type": "string", "description": "Transaction date"},
                    "description": {
                        "type": "string",
                        "description": "Transaction description",
                    },
                    "amount": {"type": "number", "description": "Transaction amount"},
                },
                "required": ["id"],
            },
        },
    }


class AccountFactory(factory.Factory):
    class Meta:
        model = Account

    pages_limit = 10
