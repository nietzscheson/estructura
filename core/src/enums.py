from enum import Enum


class AccountSubscriptionType(Enum):
    STARTUP = "STARTUP"
    PRO = "PRO"
    ENTERPRISE = "ENTERPRISE"
    FREE = "FREE"
    LIFETIME = "LIFETIME"


class AccountSubscriptionInterval(Enum):
    MONTH = "MONTH"
    YEAR = "YEAR"
    LIFETIME = "LIFETIME"


class MaxPagesPerDocument(Enum):
    ONE = "one"
    MULTIPLES = "multiples"


class DocumentStatus(Enum):
    NEW = "new"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
