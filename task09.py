# 9.1: Original predicted output: timestamp, validation only. MRO is Invoice,
# TimestampMixin, ValidateMixin, AuditMixin, Model, object; the missing super stops it.
# 9.2: Fixed output: timestamp, validation, INSERT/UPDATE, audit. Audit prints
# after its super call returns, so persistence happens first.
# 9.3: Raise an exception on invalid data; silently returning can be mistaken for
# a successful save and can let outer mixins report success.
# 9.4: Timestamp, Audit, Model, Validate prints timestamp, INSERT, audit and skips
# validation: Model terminates the chain. Put the terminal Model last.
import pytest


class Model:
    def save(self):
        print('Model.save: INSERT/UPDATE')


class TimestampMixin:
    def save(self):
        print('TimestampMixin: set updated_at')
        super().save()


class ValidateMixin:
    def save(self):
        print('ValidateMixin: validate fields')
        if not self.valid:
            raise ValueError('Invalid invoice')
        super().save()


class AuditMixin:
    def save(self):
        super().save()
        print('AuditMixin: write audit entry')


class Invoice(TimestampMixin, ValidateMixin, AuditMixin, Model):
    def __init__(self, valid=True):
        self.valid = valid


def test_order(capsys):
    assert [c.__name__ for c in Invoice.__mro__] == [
        'Invoice', 'TimestampMixin', 'ValidateMixin', 'AuditMixin', 'Model', 'object']
    Invoice().save()
    assert capsys.readouterr().out.splitlines() == [
        'TimestampMixin: set updated_at', 'ValidateMixin: validate fields',
        'Model.save: INSERT/UPDATE', 'AuditMixin: write audit entry']


def test_invalid_stops_save(capsys):
    with pytest.raises(ValueError):
        Invoice(False).save()
    output = capsys.readouterr().out
    assert 'validate fields' in output and 'INSERT' not in output and 'audit entry' not in output


def test_reordered_bases_skip_validation(capsys):
    class WrongInvoice(TimestampMixin, AuditMixin, Model, ValidateMixin):
        valid = False
    WrongInvoice().save()
    assert capsys.readouterr().out.splitlines() == [
        'TimestampMixin: set updated_at', 'Model.save: INSERT/UPDATE',
        'AuditMixin: write audit entry']


def test_original_missing_super(capsys):
    class BrokenValidateMixin:
        def save(self):
            print('ValidateMixin: validate fields')
    class OriginalInvoice(TimestampMixin, BrokenValidateMixin, AuditMixin, Model):
        pass
    OriginalInvoice().save()
    assert capsys.readouterr().out.splitlines() == [
        'TimestampMixin: set updated_at', 'ValidateMixin: validate fields']
