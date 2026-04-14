from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from .models import LedgerEntry


@dataclass
class Ledger:
    entries: List[LedgerEntry] = field(default_factory=list)

    def post_double_entry(self, debit_account: str, credit_account: str, amount: int, currency: str) -> None:
        if amount <= 0:
            raise ValueError("amount must be positive")

        self.entries.append(LedgerEntry(account=debit_account, amount=-amount, currency=currency))
        self.entries.append(LedgerEntry(account=credit_account, amount=amount, currency=currency))

    def balance(self, account: str, currency: str) -> int:
        return sum(e.amount for e in self.entries if e.account == account and e.currency == currency)

    def is_balanced(self, currency: str) -> bool:
        total = sum(e.amount for e in self.entries if e.currency == currency)
        return total == 0

    def account_balances(self, currency: str) -> Dict[str, int]:
        result: Dict[str, int] = {}
        for entry in self.entries:
            if entry.currency != currency:
                continue
            result[entry.account] = result.get(entry.account, 0) + entry.amount
        return result
