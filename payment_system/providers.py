from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import uuid4

from .models import PaymentRequest, PaymentResult, TransactionStatus


class PaymentProvider(ABC):
    name: str

    @abstractmethod
    def charge(self, request: PaymentRequest) -> PaymentResult:
        raise NotImplementedError


class SimulatedProvider(PaymentProvider):
    def __init__(self, name: str, healthy: bool = True) -> None:
        self.name = name
        self.healthy = healthy

    def charge(self, request: PaymentRequest) -> PaymentResult:
        if not self.healthy:
            return PaymentResult(
                status=TransactionStatus.FAILED,
                provider=self.name,
                reason="provider_unavailable",
            )

        return PaymentResult(
            status=TransactionStatus.SUCCESS,
            provider=self.name,
            provider_txn_id=f"{self.name}-{uuid4().hex[:12]}",
        )
