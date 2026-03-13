from ms_ovba.Views.projectLk import ProjectLk


class MockVbaProject:
    def __init__(self) -> None:
        self._license_records = []


class MockLicense:
    def to_bytes(self) -> bytes:
        return b'Test'


def test_project_lk_empty() -> None:
    vba_project = MockVbaProject()
    project_lk = ProjectLk(vba_project)

    expected = (b'\x01\x00\x00\x00\x00\x00')
    result = project_lk.to_bytes()
    assert result == expected


def test_project_lk() -> None:
    vba_project = MockVbaProject()
    mock_license = MockLicense()
    vba_project._license_records = [mock_license]
    project_lk = ProjectLk(vba_project)

    expected = (b'\x01\x00\x01\x00\x00\x00Test')
    result = project_lk.to_bytes()
    assert result == expected
