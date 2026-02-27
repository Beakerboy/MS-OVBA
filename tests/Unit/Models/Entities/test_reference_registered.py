import uuid
from ms_ovba.Models.Entities.reference_registered import ReferenceRegistered
from ms_ovba.Models.Fields.libid_reference import LibidReference


def test_constructor() -> None:
    guid = uuid.UUID('0002043000000000C000000000000046')
    ref = ref = LibidReference(
        guid,
        "2.0",
        "0",
        "C:\\Windows\\System32\\stdole2.tlb",
        "OLE Automation"
    )
    module = ReferenceRegistered("cp1", ref)
    assert isinstance(module, ReferenceRegistered)


def test_pack() -> None:
    guid = uuid.UUID('0002043000000000C000000000000046')
    ref = ref = LibidReference(
        guid,
        "2.0",
        "0",
        "C:\\Windows\\System32\\stdole2.tlb",
        "OLE Automation"
    )

    expected_hex = ("0D 00 68 00 00 00 5E 00 00 00 2A 5C 47 7B 30 30",
                    "30 32 30 34 33 30 2D 30 30 30 30 2D 30 30 30 30",
                    "2D 43 30 30 30 2D 30 30 30 30 30 30 30 30 30 30",
                    "34 36 7D 23 32 2E 30 23 30 23 43 3A 5C 00 00 00",
                    "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
                    "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
                    "00 00 00 00 00 00 00 00 00 00 00 00 00 00")
    expected = bytes.fromhex(" ".join(expected_hex))
    codepage = 0x04E4
    codepage_name = "cp" + str(codepage)
    ref_reg = ReferenceRegistered(codepage_name, ref)
    results = ref_reg.pack(codepage_name, 'little')
    assert results == expected
