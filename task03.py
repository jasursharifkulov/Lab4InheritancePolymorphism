# 3.1: Family needs super().__init__(user, months). Python does not automatically
# call an overridden parent initializer; missing attributes are discovered on access.
# 3.2: Children customize net(); the inherited price() alone applies VAT.
# 3.3: For three months: standard 168000, student 84000, family of four 369600.
# 3.4: Change Subscription.VAT_PERCENT only; no child needs editing.


class Subscription:
    VAT_PERCENT = 12
    def __init__(self, user, months):
        self.user, self.months = user, months
        self.base_monthly = 50_000
    def net(self):
        return self.base_monthly * self.months
    def price(self):
        return self.net() * (100 + self.VAT_PERCENT) // 100


class StudentSubscription(Subscription):
    def net(self):
        return super().net() // 2


class FamilySubscription(Subscription):
    def __init__(self, user, months, members):
        super().__init__(user, months)
        self.members = tuple(members)
        if not self.members:
            raise ValueError('A family must have at least one member')
    def net(self):
        return super().net() + 20_000 * (len(self.members) - 1) * self.months


def subscriptions():
    return [Subscription('Ali', 3), StudentSubscription('Ali', 3),
            FamilySubscription('Ali', 3, ['Ali', 'B', 'C', 'D'])]


def test_prices():
    assert [s.price() for s in subscriptions()] == [168000, 84000, 369600]


def test_shared_vat(monkeypatch):
    monkeypatch.setattr(Subscription, 'VAT_PERCENT', 15)
    assert [s.price() for s in subscriptions()] == [172500, 86250, 379500]
