from ms_ovba.Models.Fields.doubleEncodedString import (
    DoubleEncodedString
)


def test_constructor() -> None:
    de_string = DoubleEncodedString([0x01, 0x02], "Foo")
    assert isinstance(de_string, DoubleEncodedString)


def test_value_property() -> None:
    expected = "Foo"
    de_string = DoubleEncodedString([0x01, 0x02], expected)
    assert de_string.value == expected


def test_pack() -> None:
    de_string = DoubleEncodedString([0x01, 0x02], "Foo")
    expected = (b'\x01\x00\x03\x00\x00\x00Foo' +
                b'\x02\x00\x06\x00\x00\x00F\x00o\x00o\x00')
