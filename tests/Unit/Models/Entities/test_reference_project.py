from ms_ovba.Models.Entities.reference_project import ReferenceProject
from ms_ovba.Models.Fields.project_reference import ProjectReference


def test_constructor() -> None:
    ref = ProjectReference("C:/")
    module = ReferenceProject("cp1", ref)

    assert isinstance(module, ReferenceProject)

def test_pack() -> None:
    ref = ProjectReference("")

    module_cache.indirect_table = bytes.fromhex(" ".join(indirect_table))
    expected_hex = ("00 0E 00 00 00 5E 00 00 00 30 2A 5C 43 43 3A 5C",
                    "45 78 61 6D 70 6C 65 20 50 61 74 68 5C 45 78 61",
                    "6D 70 6C 65 2D 52 65 66 65 72 65 6E 63 65 64 50",
                    "72 6F 6A 65 63 74 2E 78 6C 73 00 00 00 20 2A 5C",
                    "43 45 78 61 6D 70 6C 65 2D 52 65 66 65 72 65 6E",
                    "63 65 64 50 72 6F 6A 65 63 74 2E 78 6C 73 49 A9",
                    "5F 46 00 0D")
    expected = bytes.fromhex(" ".join(expected_hex))
    codepage = 0x04E4
    codepage_name = "cp" + str(codepage)
    module = ReferenceProject(codepage_name, ref)
    results = module.pack(codepage_name, 'little')
    assert results == expected
