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
    ref_twid = MockLibIdTwid()
    ref_extend = MockLibIdExt()
    ref = ReferenceControl(ref_twid, ref_extend, guid, 1, "MSForms")

    expected_hex = ("2F 00 3B 00 00 00 31 00 00 00 2A 5C 47 7B 30 30",
                    "30 30 30 30 30 30 2D 30 30 30 30 2D 30 30 30 30",
                    "2D 30 30 30 30 2D 30 30 30 30 30 30 30 30 30 30",
                    "30 30 7D 23 30 2E 30 23 30 23 23 00 00 00 00 00",
                    "00 16 00 07 00 00 00 4D 53 46 6F 72 6D 73 3E 00",
                    "0E 00 00 00 4D 00 53 00 46 00 6F 00 72 00 6D 00",
                    "73 00 30 00 A3 00 00 00 85 00 00 00 2A 5C 47 7B",
                    "38 39 36 43 32 44 38 33 2D 35 34 36 36 2D 34 36",
                    "45 44 2D 38 46 41 45 2D 34 43 33 45 34 46 38 35",
                    "45 37 31 30 7D 23 32 2E 30 23 30 23 43 3A 5C 55",
                    "73 65 72 73 5C 6A 73 6D 69 74 68 5C 41 70 70 44",
                    "61 74 61 5C 4C 6F 63 61 6C 5C 54 65 6D 70 5C 56",
                    "42 45 5C 4D 53 46 6F 72 6D 73 2E 65 78 64 23 4D",
                    "69 63 72 6F 73 6F 66 74 20 46 6F 72 6D 73 20 32",
                    "2E 30 20 4F 62 6A 65 63 74 20 4C 69 62 72 61 72",
                    "79 00 00 00 00 00 00 E1 2E 45 0D 8F E0 1A 10 85",
                    "2E 02 60 8C 4D 0B B4")
    expected = bytes.fromhex(" ".join(expected_hex))
    codepage = 0x04E4
    cp_name = "cp" + str(codepage)
    path = 'ms_ovba.Models.Entities.reference.DoubleEncodedString'
    with mock.patch(path, MockDEString):
        results = ref.pack('little', cp_name)
        assert results == expected
