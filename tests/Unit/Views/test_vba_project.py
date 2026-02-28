from ms_ovba.Views.project_view import ProjectView


class MockVbaProject():

    def __init__(self) -> None:
        self.endien = 'little'
        self.performance_cache = b''
        self.performance_cache_version = 0xFFFF

    def get_performance_cache(self) -> bytes:
        return self.performance_cache

    def get_performance_cache_version(self):
        return self.performance_cache_version


def test_vba_project_default() -> None:
    vba_project = MockVbaProject()
    vba_project_view = ProjectView(vba_project)
    expected = b'\xCC\x61\xFF\xFF\x00\x03\x00'
    assert vba_project_view.to_bytes() == expected


def test_vba_project() -> None:
    """
    Demonstrate the effect of performance cache on the project
    """
    vba_project = MockVbaProject()
    vba_project.performance_cache = b'\x00\x01\x02\x03'
    vba_project.performance_cache_version = 0x00B5
    
    vba_project_view = ProjectView(vba_project)
    expected = b'\xCC\x61\xB5\x00\x00\x03\x00\x00\x01\x02\x03'
    assert vba_project_view.to_bytes() == expected
