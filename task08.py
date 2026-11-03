# 8.1: The second search definition replaces the first in the class namespace.
# Calling it without filters therefore raises TypeError; Python does not overload
# methods by their argument signatures.
# 8.2: None avoids sharing a mutable dictionary between calls.
# 8.3: A keyword-only filters dictionary separates filters from other future options
# and supports dynamic keys. Both unfiltered and filtered calls work.
# 8.4: pyflakes reports redefinition of unused 'search'; original in experiments/.


class ProductSearch:
    def __init__(self, products):
        self.products = products
    def search(self, query, *, filters=None):
        q = query.lower()
        result = [p for p in self.products if q in p['title'].lower()]
        for key, value in (filters or {}).items():
            result = [p for p in result if p.get(key) == value]
        return result


def test_both_calls():
    products = [{'title': 'iPhone 15', 'brand': 'Apple'},
                {'title': 'iPhone case', 'brand': 'Other'}]
    ps = ProductSearch(products)
    assert ps.search('IPHONE') == products
    filters = {'brand': 'Apple'}
    assert ps.search('iphone', filters=filters) == [products[0]]
    assert filters == {'brand': 'Apple'}
    assert ps.search('iphone') == products
    assert ps.search('unknown') == []
