# 1.1: PaymentMethod defines the fee and refund contract.
# 1.2: Click and Payme are separate classes: independent providers can change separately.
# 1.3: Checkout delegates to the object's behaviour instead of inspecting its type.
# 1.4: BankTransfer required zero changed lines in Checkout or other existing classes.
from abc import ABC, abstractmethod
import pytest


class PaymentMethod(ABC):
    @abstractmethod
    def fee(self, amount: int) -> int: ...

    @property
    @abstractmethod
    def refundable(self) -> bool: ...


class Card(PaymentMethod):
    refundable = True

    def fee(self, amount: int) -> int:
        return amount * 15 // 1000


class Click(PaymentMethod):
    refundable = True

    def fee(self, amount: int) -> int:
        return amount * 10 // 1000


class Payme(PaymentMethod):
    refundable = True

    def fee(self, amount: int) -> int:
        return amount * 10 // 1000


class Cash(PaymentMethod):
    refundable = False

    def fee(self, amount: int) -> int:
        return 0


class BankTransfer(PaymentMethod):
    refundable = True

    def fee(self, amount: int) -> int:
        return 5_000


class Checkout:
    def pay(self, method: PaymentMethod, amount: int) -> dict:
        return {'charged': amount + method.fee(amount), 'refundable': method.refundable}


@pytest.mark.parametrize('method,charged,refundable', [
    (Card(), 101500, True), (Click(), 101000, True),
    (Payme(), 101000, True), (Cash(), 100000, False),
    (BankTransfer(), 105000, True),
])
def test_methods(method, charged, refundable):
    assert Checkout().pay(method, 100000) == {'charged': charged, 'refundable': refundable}


def test_new_provider_without_checkout_changes():
    class NewProvider(PaymentMethod):
        refundable = False
        def fee(self, amount):
            return 42
    assert Checkout().pay(NewProvider(), 100)['charged'] == 142
