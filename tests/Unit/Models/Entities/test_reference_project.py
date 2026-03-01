from ms_ovba.Models.Entities.reference_project import ReferenceProject


def test_constructor() -> None:
    ref = MockProjectReference()
    module = ReferenceProject("cp1", ref)
    assert isinstance(module, ReferenceProject)


class MockProjectReference2:
    def __len__():
        return 0x0020

    def __str__(self):
        return "*\\CExample-ReferencedProject.xls"


class MockProjectReference:
    def __len__():
        return 0x0030

    def __str__(self):
        return "*\\CC:\\Example Path\\Example-ReferencedProject.xls"

    def relative(self):
        return MockProjectReference2()


def test_pack() -> None:
    ref = MockProjectReference()

    expected_hex = ("0E 00 5E 00 00 00 30 00 00 00 2A 5C 43 43 3A 5C",
                    "45 78 61 6D 70 6C 65 20 50 61 74 68 5C 45 78 61",
                    "6D 70 6C 65 2D 52 65 66 65 72 65 6E 63 65 64 50",
                    "72 6F 6A 65 63 74 2E 78 6C 73 20 00 00 00 2A 5C",
                    "43 45 78 61 6D 70 6C 65 2D 52 65 66 65 72 65 6E",
                    "63 65 64 50 72 6F 6A 65 63 74 2E 78 6C 73 57 02",
                    "BE 65 17 00")
    expected = bytes.fromhex(" ".join(expected_hex))
    codepage = 0x04E4
    codepage_name = "cp" + str(codepage)
    ref_proj = ReferenceProject(codepage_name, ref)
    results = ref_proj.pack(codepage_name, 'little')
    assert results == expected
