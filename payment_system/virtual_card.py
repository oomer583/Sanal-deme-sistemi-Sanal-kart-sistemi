from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict
from uuid import uuid4


@dataclass
class VirtualCard:
    card_id: str
    user_id: str
    masked_pan: str
    expiry_month: int
    expiry_year: int
    cvv_token: str
    status: str
    spending_limit: int


class VirtualCardService:
    def __init__(self) -> None:
        self.cards: Dict[str, VirtualCard] = {}

    def create_card(self, user_id: str, spending_limit: int) -> VirtualCard:
        now = datetime.utcnow()
        expiry = now + timedelta(days=365 * 3)
        card = VirtualCard(
            card_id=uuid4().hex,
            user_id=user_id,
            masked_pan=f"4111 **** **** {str(uuid4().int)[-4:]}",
            expiry_month=expiry.month,
            expiry_year=expiry.year,
            cvv_token=uuid4().hex[:6],
            status="active",
            spending_limit=spending_limit,
        )
        self.cards[card.card_id] = card
        return card

    def freeze_card(self, card_id: str) -> None:
        card = self.cards[card_id]
        card.status = "frozen"

    def unfreeze_card(self, card_id: str) -> None:
        card = self.cards[card_id]
        card.status = "active"

    def update_limit(self, card_id: str, new_limit: int) -> None:
        if new_limit <= 0:
            raise ValueError("new_limit must be positive")
        card = self.cards[card_id]
        card.spending_limit = new_limit
