# 4.1: AuditLog is not a substitutable mutable list: clear, pop and sort break its contract.
# 4.2: It owns a private list and exposes only append-oriented operations/read views.
# 4.3: Entries are tuples of immutable strings. last() returns a tuple snapshot.
# 4.4: There are 11 non-underscore public list methods (checked below), plus mutation
# special methods. Blocking selected methods is fragile and list.clear(log) can bypass
# an override. Composition avoids exposing the list API; it is not tamper-proof storage.
import pytest


class AuditLog:
    def __init__(self):
        self.__entries = []
    def record(self, user: str, action: str):
        if not isinstance(user, str) or not isinstance(action, str):
            raise TypeError('Audit fields must be strings')
        self.__entries.append((user, action))
    def __len__(self):
        return len(self.__entries)
    def __iter__(self):
        return iter(tuple(self.__entries))
    def last(self, n):
        if n < 0:
            raise ValueError('n must not be negative')
        return tuple(self.__entries[-n:]) if n else ()


def test_append_and_read():
    log = AuditLog()
    log.record('admin', 'approve')
    snapshot = log.last(1)
    log.record('user', 'view')
    assert len(log) == 2
    assert list(log) == [('admin', 'approve'), ('user', 'view')]
    assert snapshot == (('admin', 'approve'),)
    assert log.last(0) == ()
    assert log.last(10) == tuple(log)
    with pytest.raises(ValueError):
        log.last(-1)


def test_mutation_is_not_exposed():
    log = AuditLog()
    log.record('a', 'b')
    for name in ('clear', 'sort', 'pop', 'append'):
        with pytest.raises(AttributeError):
            getattr(log, name)
    with pytest.raises(TypeError):
        log[0] = ('x', 'y')
    with pytest.raises(TypeError):
        log.last(1)[0][0] = 'changed'
    assert len([name for name in dir(list) if not name.startswith('_')]) == 11
