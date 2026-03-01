from ms_ovba.Models.Entities.reference import Reference
from unittest import mock


class MockDEString:
    def pack(self, one, two) -> bytes:
        return b'VBAProject\x16\x00\x00\x00V\x00B\x00A\x00P\x00r\x00o\x00j\x00e\x00c\x00t\x00'


class MockRefProj:
    def pack(self, foo, bar) -> bytes:
        return b''


def test_constructor1() -> None:
    ref_proj = ""
    ref = Reference("cp1", ref_proj)
    assert isinstance(ref, Reference)


def test_constructor2() -> None:
    ref = Reference("cp1", "", "VBAProject1")
    assert isinstance(ref, Reference)


def test_pack() -> None:
    ref_proj = MockRefProj()
    ref = Reference("cp1", ref_proj, "VBAProject1")

    expected_hex = ("16 00 0B 00 00 00 56 42 41 50 72 6F 6A 65 63 74",
                    "31 3E 00 16 00 00 00 56 00 42 00 41 00 50 00 72",
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
    codepage_name = "cp" + str(codepage)
    path = 'ms_ovba.Models.Entities.reference.DoubleEncodedString'
    with mock.patch(path, MockDEString):
        results = ref.pack(codepage_name, 'little')
        assert results == expected
