from ms_ovba.Models.Entities.reference_project import ReferenceProject


def test_constructor() -> None:
    ref = MockProjectReference()
    module = ReferenceProject(ref)
    assert isinstance(module, ReferenceProject)


mock_proj1 = mock.MagicMock()
mock_proj1.__len__.return_value = 0x20
mock_proj1.__str__.return_value = (
    r"*\CExample-ReferencedProject.xls"
)


mock_proj = mock.MagicMock()
mock_proj.__len__.return_value = 0x30
mock_proj.__str__.return_value = (
    r"*\CC:\Example Path\Example-ReferencedProject.xls"
)
mock_proj.relative.return_value =mock_proj1


def test_pack() -> None:
    expected_hex = ("0E 00 5E 00 00 00 30 00 00 00 2A 5C 43 43 3A 5C",
                    "45 78 61 6D 70 6C 65 20 50 61 74 68 5C 45 78 61",
                    "6D 70 6C 65 2D 52 65 66 65 72 65 6E 63 65 64 50",
                    "72 6F 6A 65 63 74 2E 78 6C 73 20 00 00 00 2A 5C",
                    "43 45 78 61 6D 70 6C 65 2D 52 65 66 65 72 65 6E",
                    "63 65 64 50 72 6F 6A 65 63 74 2E 78 6C 73 57 02",
                    "BE 65 17 00")
    expected = bytes.fromhex(" ".join(expected_hex))
    codepage = 0x04E4
    cp_name = "cp" + str(codepage)
    ref_proj = ReferenceProject(mock_proj)
    results = ref_proj.pack('little', cp_name)
    assert results == expected
