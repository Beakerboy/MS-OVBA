import uuid
from ms_ovba.Models.Entities.reference_registered import ReferenceRegistered
from ms_ovba.Models.Fields.libid_reference import LibidReference


class MockLibid:
    pass


def test_constructor() -> None:
    ref = MockLibid()
    module = ReferenceRegistered("cp1", ref)
    assert isinstance(module, ReferenceRegistered)


def test_pack() -> None:
    guid = uuid.UUID('0002043000000000C000000000000046')
    ref = LibidReference(
        guid,
        "2.0",
        "0",
        "C:\\Windows\\system32\\stdole2.tlb",
        "OLE Automation"
    )

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
    ref_reg = ReferenceRegistered(codepage_name, ref)
    results = ref_reg.pack(codepage_name, 'little')
    assert results == expected


def test_unpack() -> None:
    hex = ("0D 00 68 00 00 00 5E 00 00 00 2A 5C 47 7B 30 30",
           "30 32 30 34 33 30 2D 30 30 30 30 2D 30 30 30 30",
           "2D 43 30 30 30 2D 30 30 30 30 30 30 30 30 30 30",
           "34 36 7D 23 32 2E 30 23 30 23 43 3A 5C 57 69 6E",
           "64 6F 77 73 5C 73 79 73 74 65 6D 33 32 5C 73 74",
           "64 6F 6C 65 32 2E 74 6C 62 23 4F 4C 45 20 41 75",
           "74 6F 6D 61 74 69 6F 6E 00 00 00 00 00 00")
    data = bytes.fromhex(" ".join(hex))
    ref = ReferenceRegistered.unpack(data, "little")
    assert isinstance(ref.libid, LibidReference)
