from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class TransactionStatus(str, Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"


@dataclass(frozen=True)
class PaymentRequest:
    user_id: str
    amount: int
    currency: str
    merchant_id: str
    idempotency_key: str


@dataclass
class PaymentResult:
    status: TransactionStatus
    provider: Optional[str] = None
    provider_txn_id: Optional[str] = None
    reason: Optional[str] = None


@dataclass
class LedgerEntry:
    account: str
    amount: int
    currency: str
    created_at: datetime = field(default_factory=datetime.utcnow)
