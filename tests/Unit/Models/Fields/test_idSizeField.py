import pytest
from ms_ovba.Models.Fields.idSizeField import IdSizeField


def test_string() -> None:
    field = IdSizeField(1, 2, "Hi")
    expected = b'\x01\x00\x02\x00\x00\x00Hi'
    assert field.pack("little") == expected


def test_H() -> None:
    field = IdSizeField(1, 2, 3)
    expected = b'\x01\x00\x02\x00\x00\x00\x03\x00'
    assert field.pack("little") == expected


def test_I() -> None:
    field = IdSizeField(1, 4, 3)
    expected = b'\x01\x00\x04\x00\x00\x00\x03\x00\x00\x00'
    assert field.pack("little") == expected


def test_bad_value() -> None:
    field = IdSizeField(2, 3, 6)
    with pytest.raises(Exception):
        field.pack("little")
