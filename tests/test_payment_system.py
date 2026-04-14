import unittest

from payment_system.models import PaymentRequest, TransactionStatus
from payment_system.providers import SimulatedProvider
from payment_system.service import PaymentService
from payment_system.virtual_card import VirtualCardService


class PaymentServiceTests(unittest.TestCase):
    def test_failover_to_second_provider(self) -> None:
        service = PaymentService(
            providers=[
                SimulatedProvider("provider_a", healthy=False),
                SimulatedProvider("provider_b", healthy=True),
            ]
        )
        request = PaymentRequest(
            user_id="u1",
            amount=1000,
            currency="TRY",
            merchant_id="m1",
            idempotency_key="idem-1",
        )

        result = service.process_payment(request)

        self.assertEqual(result.status, TransactionStatus.SUCCESS)
        self.assertEqual(result.provider, "provider_b")
        self.assertTrue(service.ledger.is_balanced("TRY"))

    def test_idempotency_returns_same_result(self) -> None:
        service = PaymentService(providers=[SimulatedProvider("provider_a", healthy=True)])
        request = PaymentRequest(
            user_id="u1",
            amount=1000,
            currency="TRY",
            merchant_id="m1",
            idempotency_key="idem-2",
        )

        first = service.process_payment(request)
        second = service.process_payment(request)

        self.assertEqual(first.provider_txn_id, second.provider_txn_id)
        self.assertEqual(len(service.ledger.entries), 2)


class VirtualCardTests(unittest.TestCase):
    def test_card_lifecycle(self) -> None:
        cards = VirtualCardService()
        card = cards.create_card(user_id="u1", spending_limit=5000)

        self.assertEqual(card.status, "active")
        cards.freeze_card(card.card_id)
        self.assertEqual(cards.cards[card.card_id].status, "frozen")
        cards.unfreeze_card(card.card_id)
        self.assertEqual(cards.cards[card.card_id].status, "active")

    def test_update_limit_validation(self) -> None:
        cards = VirtualCardService()
        card = cards.create_card(user_id="u1", spending_limit=5000)

        with self.assertRaises(ValueError):
            cards.update_limit(card.card_id, 0)


if __name__ == "__main__":
    unittest.main()
