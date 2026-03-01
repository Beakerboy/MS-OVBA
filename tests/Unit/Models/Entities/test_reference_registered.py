from unittest import mock
from ms_ovba.Models.Entities.reference_registered import ReferenceRegistered


class MockLibid1:
    def __len__(self):
        return 0x005E

    def __str__(self):
        return ("*\\G{00020430-0000-0000-C000-000000000046}#2.0#0#" +
                "C:\\Windows\\system32\\stdole2.tlb#OLE Automation")


class MockLibid2:

    @staticmethod
    def unpack(data, endien):
        lib = MockLibid2()
        lib.data = data
        return lib


def test_constructor() -> None:
    ref = MockLibid1()
    module = ReferenceRegistered("cp1", ref)
    assert isinstance(module, ReferenceRegistered)


def test_pack() -> None:
    expected_hex = ("0D 00 68 00 00 00 5E 00 00 00 2A 5C 47 7B 30 30",
                    "30 32 30 34 33 30 2D 30 30 30 30 2D 30 30 30 30",
                    "2D 43 30 30 30 2D 30 30 30 30 30 30 30 30 30 30",
                    "34 36 7D 23 32 2E 30 23 30 23 43 3A 5C 57 69 6E",
                    "64 6F 77 73 5C 73 79 73 74 65 6D 33 32 5C 73 74",
                    "64 6F 6C 65 32 2E 74 6C 62 23 4F 4C 45 20 41 75",
                    "74 6F 6D 61 74 69 6F 6E 00 00 00 00 00 00")
    expected = bytes.fromhex(" ".join(expected_hex))
    codepage = 0x04E4
    codepage_name = "cp" + str(codepage)
    ref_reg = ReferenceRegistered(codepage_name, MockLibid1())
    results = ref_reg.pack(codepage_name, 'little')
    assert results == expected


def test_unpack():
    hex = ("0D 00 68 00 00 00 5E 00 00 00 2A 5C 47 7B 30 30",
           "30 32 30 34 33 30 2D 30 30 30 30 2D 30 30 30 30",
           "2D 43 30 30 30 2D 30 30 30 30 30 30 30 30 30 30",
           "34 36 7D 23 32 2E 30 23 30 23 43 3A 5C 57 69 6E",
           "64 6F 77 73 5C 73 79 73 74 65 6D 33 32 5C 73 74",
           "64 6F 6C 65 32 2E 74 6C 62 23 4F 4C 45 20 41 75",
           "74 6F 6D 61 74 69 6F 6E 00 00 00 00 00 00")
    data = bytes.fromhex(" ".join(hex))
    path = 'ms_ovba.Models.Entities.reference_registered.LibidReference'
    with mock.patch(path, MockLibid2):
        ref = ReferenceRegistered.unpack(data, "little")
        assert ref.libid.data == (b'*{00020430-0000-0000-C000-000000000046}' +
                                  b'#2.0#0#' +
                                  b'C:\\Windows\\system32\\stdole2.tlb#' +
                                  b'OLE Automation')
