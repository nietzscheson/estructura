from src.enums import DocumentStatus
from src.mixins.state_machine import StateMachineMixin  # el mixin anterior
from src.models import Document
from transitions import Machine


class DocumentFSMService(StateMachineMixin):
    def __init__(self, document: Document):
        self.document = document
        self.status = document.status  # copia inicial del estado

        self.machine = Machine(
            model=self,
            states=[s.value for s in DocumentStatus],
            transitions=[
                {"trigger": "created", "source": "NEW", "dest": "RECEIVED"},
                {
                    "trigger": "start_processing",
                    "source": "RECEIVED",
                    "dest": "PROCESSING",
                },
                {"trigger": "complete", "source": "PROCESSING", "dest": "COMPLETED"},
                {"trigger": "fail", "source": "*", "dest": "FAILED"},
            ],
            initial=self.status,
        )

    def sync(self):
        self.document.status = self.status
