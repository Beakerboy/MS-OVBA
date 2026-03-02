import pytest
from ms_ovba.Models.Fields.idSizeField import IdSizeField


def test_H():
    field = IdSizeField(1, 2, 3)
    assert field.pack("cp", "little") == b'\x01\x00\x01\x00\x00\x00\x03\x00'


def test_I():
    field = IdSizeField(1, 4, 3)
    assert field.pack("cp", "little") == b'\x01\x00\x01\x00\x00\x00\x03\x00\x00\x00'


def test_bad_value() -> None:
    field = IdSizeField(2, 3, 6)
    with pytest.raises(Exception):
        field.pack(1234, "little")
