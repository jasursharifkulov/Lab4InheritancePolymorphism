# 7.1: frozen dataclass gives an immutable value. order=True compares fields in order
# and would order USD and UZS by amount without rejecting unlike currencies.
# 7.2: sum starts at integer zero; __radd__ accepts only that identity value.
# In production prefer sum(items, Money(0, 'UZS')) to preserve currency for empty lists.
# 7.3: Unsupported operands return NotImplemented, allowing reflected operations
# and equality fallback (Money == int ultimately becomes False).
# 7.4: Only integer quantity multiplication is supported. Money*Money and Money/Money
# are omitted because their dimensions/return types need a separate explicit contract.
from dataclasses import dataclass, FrozenInstanceError
from functools import total_ordering
import pytest


class CurrencyMismatchError(ValueError):
    pass


@total_ordering
@dataclass(frozen=True, eq=False)
class Money:
    amount: int
    currency: str
    def __post_init__(self):
        if type(self.amount) is not int:
            raise TypeError('amount must be an integer in minor units')
        if not (isinstance(self.currency, str) and len(self.currency) == 3
                and self.currency.isascii() and self.currency.isalpha()
                and self.currency.isupper()):
            raise ValueError('currency must be three uppercase ASCII letters')
    def _same_currency(self, other):
        if self.currency != other.currency:
            raise CurrencyMismatchError(f'{self.currency} != {other.currency}')
    def __add__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        self._same_currency(other)
        return Money(self.amount + other.amount, self.currency)
    def __radd__(self, other):
        if type(other) is int and other == 0:
            return self
        return NotImplemented
    def __mul__(self, quantity):
        if type(quantity) is not int:
            return NotImplemented
        return Money(self.amount * quantity, self.currency)
    def __rmul__(self, quantity):
        return self * quantity
    def __eq__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        return (self.amount, self.currency) == (other.amount, other.currency)
    def __lt__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        self._same_currency(other)
        return self.amount < other.amount
    def __hash__(self):
        return hash((self.amount, self.currency))


def test_money_operations():
    a, b = Money(500, 'UZS'), Money(200, 'UZS')
    assert a + b == sum([a, b]) == Money(700, 'UZS')
    assert a * 3 == 3 * a == Money(1500, 'UZS')
    assert b < a and a > b and a >= b and b <= a
    assert a != 500 and a != Money(500, 'USD')
    assert {a: 'price'}[Money(500, 'UZS')] == 'price'
    assert sum([], Money(0, 'UZS')) == Money(0, 'UZS')
    assert a.__add__(1) is NotImplemented and a.__eq__(1) is NotImplemented
    with pytest.raises(FrozenInstanceError):
        a.amount = 1


def test_currency_and_operand_errors():
    with pytest.raises(CurrencyMismatchError):
        Money(100, 'USD') + Money(1, 'UZS')
    with pytest.raises(CurrencyMismatchError):
        Money(100, 'USD') > Money(1, 'UZS')
    with pytest.raises(TypeError):
        Money(1, 'UZS') * Money(2, 'UZS')
    with pytest.raises(TypeError):
        Money(1, 'UZS') + 1
    with pytest.raises(TypeError):
        Money(1.5, 'UZS')
    with pytest.raises(ValueError):
        Money(1, 'usd')


def test_automatic_order_is_wrong_for_money():
    @dataclass(order=True)
    class AutomaticallyOrderedMoney:
        amount: int
        currency: str
    # This succeeds instead of rejecting incompatible currencies.
    assert AutomaticallyOrderedMoney(100, 'USD') > AutomaticallyOrderedMoney(1, 'UZS')
