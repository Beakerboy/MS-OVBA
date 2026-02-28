from ms_ovba.Views.projectWm import ProjectWm


class Mod:
    def __init__(self, name) -> None:
        self.modName.value = name


class MockVbaProject:
    def __init__(self) -> None:
        self.modules = [Mod("ThisWorkbook"), Mod("Sheet1"), Mod("Module1")]


def test_project_wm() -> None:
    vba_project = MockVbaProject()
    project_wm = ProjectWm(vba_project)

    expected = (b'ThisWorkbook\x00T\x00h\x00i\x00s\x00W\x00o\x00r\x00k\x00b'
                + b'\x00o\x00o\x00k\x00\x00\x00Sheet1\x00S\x00h\x00e\x00e\x00'
                + b't\x001\x00\x00\x00Module1\x00M\x00o\x00d\x00u\x00l\x00e'
                + b'\x001\x00\x00\x00\x00\x00')
    result = project_wm.to_bytes()
    assert len(result) == 86
    assert result == expected
