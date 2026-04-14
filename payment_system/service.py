from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from .ledger import Ledger
from .models import PaymentRequest, PaymentResult, TransactionStatus
from .providers import PaymentProvider


@dataclass
class PaymentService:
    providers: List[PaymentProvider]
    ledger: Ledger = field(default_factory=Ledger)
    _idem_store: Dict[str, PaymentResult] = field(default_factory=dict)

    def process_payment(self, request: PaymentRequest) -> PaymentResult:
        cached = self._idem_store.get(request.idempotency_key)
        if cached:
            return cached

        for provider in self.providers:
            result = provider.charge(request)
            if result.status == TransactionStatus.SUCCESS:
                self.ledger.post_double_entry(
                    debit_account=f"user:{request.user_id}",
                    credit_account=f"merchant:{request.merchant_id}",
                    amount=request.amount,
                    currency=request.currency,
                )
                self._idem_store[request.idempotency_key] = result
                return result

        failed = PaymentResult(status=TransactionStatus.FAILED, reason="all_providers_failed")
        self._idem_store[request.idempotency_key] = failed
        return failed
