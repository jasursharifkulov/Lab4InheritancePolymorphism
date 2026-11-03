# 6.1: The target needs write(bytes), not file ancestry. All targets below consume
# every supplied byte, as assumed by this simple exporter.
# 6.2-3: Protocol describes structural compatibility; no inheritance/type check needed.
# 6.4: A missing write raises AttributeError when a nonempty report is exported.
# mypy catches an incompatible target before runtime; see experiments/bad_target.py.
import io
from typing import Iterable, Protocol
import pytest


class Writable(Protocol):
    def write(self, data: bytes) -> int: ...


def export_report(rows: Iterable[Iterable[object]], target: Writable) -> None:
    for row in rows:
        target.write((','.join(map(str, row)) + '\n').encode())


class S3Upload:
    def __init__(self, bucket: str, key: str) -> None:
        self.bucket, self.key = bucket, key
        self.parts: list[bytes] = []
    def write(self, data: bytes) -> int:
        self.parts.append(data)
        return len(data)


class FakeTarget:
    def __init__(self) -> None:
        self.data = b''
    def write(self, data: bytes) -> int:
        self.data += data
        return len(data)


def test_targets() -> None:
    memory = io.BytesIO()
    cloud = S3Upload('reports', 'sales.csv')
    fake = FakeTarget()
    targets: list[Writable] = [memory, cloud, fake]
    for target in targets:
        export_report([[1, 'Ali'], [2, 'Vali']], target)
    expected = b'1,Ali\n2,Vali\n'
    assert memory.getvalue() == b''.join(cloud.parts) == fake.data == expected


def test_missing_write() -> None:
    with pytest.raises(AttributeError):
        export_report([[1]], object())  # type: ignore[arg-type]
