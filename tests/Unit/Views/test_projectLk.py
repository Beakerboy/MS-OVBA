from ms_ovba.Views.projectLk import ProjectLk


class MockVbaProject:
    def __init__(self) -> None:
        self.licenses = []


def test_project_lk() -> None:
    vba_project = MockVbaProject()
    project_lk = ProjectLk(vba_project)

    expected = (b'\x01\x00\x00\x00\x00\x00')
    result = project_lk.to_bytes()
    assert result == expected
