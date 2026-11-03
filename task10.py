# 10.1-3: One boundary registry normalizes names and creates polymorphic objects.
# 10.4: Translating external names is a boundary responsibility; Checkout only
# depends on behaviour, so provider selection is not repeated throughout the system.
# 10.5: After defining BankTransfer in Task 1, adding it here changes one registry
# entry and zero Checkout lines. Supported names are derived from the mapping.
from task01 import PaymentMethod, Card, Click, Payme, Cash, BankTransfer, Checkout
import pytest


class UnknownPaymentMethodError(ValueError):
    pass


REGISTRY: dict[str, type[PaymentMethod]] = {
    'card': Card, 'click': Click, 'payme': Payme,
    'cash': Cash, 'bank_transfer': BankTransfer,
}


def create_payment_method(name: str) -> PaymentMethod:
    key = name.strip().lower()
    try:
        factory = REGISTRY[key]
    except KeyError:
        raise UnknownPaymentMethodError(
            f'Unknown payment method {name!r}. Supported: {", ".join(sorted(REGISTRY))}'
        ) from None
    return factory()


@pytest.mark.parametrize('name', [' Payme ', 'PAYME', 'payme'])
def test_normalization(name):
    assert isinstance(create_payment_method(name), Payme)


def test_unknown_and_bank():
    with pytest.raises(UnknownPaymentMethodError) as error:
        create_payment_method('crypto')
    for name in REGISTRY:
        assert name in str(error.value)
    assert Checkout().pay(create_payment_method('bank_transfer'), 100000) == {
        'charged': 105000, 'refundable': True}
