import uuid
from ms_ovba.Models.Entities.reference_control import ReferenceControl
from unittest import mock


class MockDEString:
    def __init__(self, foo, bar) -> None:
        pass

    def pack(self, one, two) -> bytes:
        return (b'\x16\x00\x0B\x00\x00\x00VBAProject1' +
                b'\x3E\x00\x16\x00\x00\x00V\x00B\x00A\x00P\x00r' +
                b'\x00o\x00j\x00e\x00c\x00t\x001\x00')


class MockLibIdExt:
    def __str__(self) -> str:
        return (
            "*\\G{896C2D83-5466-46ED-8FAE-4C3E4F85E710}#2.0#" +
            "0#C:\\Users\\jsmith\\AppData\\Local\\Temp\\VBE\\MSForms.exd#" +
            "Microsoft Forms 2.0 Object Library"
        )


class MockLibIdTwid:
    def __str__(self):
        return "*\\G{00000000-0000-0000-0000-000000000000}#0.0#0##"


guid = uuid.UUID('896C2D83546646ED8FAE4C3E4F85E710')


def test_constructor() -> None:
    ref1 = MockLibIdTwid()
    ref2 = MockLibIdExt()
    cookie = 2
    ref = ReferenceControl(ref1, ref2, guid, cookie)
    assert isinstance(ref, ReferenceControl)


def test_constructor1() -> None:
    ref1 = ""
    ref2 = ""
    cookie = 2
    name = "Test"
    ref = ReferenceControl(ref1, ref2, guid, cookie, name)
    assert isinstance(ref, ReferenceControl)


def test_pack() -> None:
    ref_twid = MockLibIdExt()
    ref_extend = MockLibIdExt()
    ref = ReferenceControl(ref_twid, ref_extend, guid, 1, "VBAProject1")

    expected_hex = ("2F 00 3B 00 00 00 31 00 00 00 2A 5C 47 7B 00 00",
                    "00 00 00 00 00 00 2D 00 00 00 00 2D 00 50 00 72",
                    "00 6F 00 6A 00 65 00 63 00 74 00 31 00 0E 00 5E",
                    "00 00 00 30 00 00 00 2A 5C 43 43 3A 5C 45 78 61",
                    "6D 70 6C 65 20 50 61 74 68 5C 45 78 61 6D 70 6C",
                    "65 2D 52 65 66 65 72 65 6E 63 65 64 50 72 6F 6A",
                    "65 63 74 2E 78 6C 73 20 00 00 00 2A 5C 43 45 78",
                    "61 6D 70 6C 65 2D 52 65 66 65 72 65 6E 63 65 64",
                    "50 72 6F 6A 65 63 74 2E 78 6C 73 57 02 BE 65 17",
                    "00")
    expected = bytes.fromhex(" ".join(expected_hex))
    codepage = 0x04E4
    cp_name = "cp" + str(codepage)
    path = 'ms_ovba.Models.Entities.reference.DoubleEncodedString'
    with mock.patch(path, MockDEString):
        results = ref.pack('little', cp_name)
        assert results == expected
