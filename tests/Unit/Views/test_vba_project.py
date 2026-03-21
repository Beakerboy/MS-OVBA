from ms_ovba.Views.project_view import ProjectView
from unittest import mock


mock_vbaproject = mock.Mock()


def test_vba_project_default() -> None:
    pcv = mock.PropertyMock(return_value=0xFFFF)
    pc = mock.PropertyMock(return_value=b'')
    type(mock_vbaproject).performance_cache_version = pcv
    type(mock_vbaproject).performance_cache = pc
    vba_project_view = ProjectView(mock_vbaproject)
    expected = b'\xCC\x61\xFF\xFF\x00\x03\x00'
    assert vba_project_view.to_bytes() == expected


def test_vba_project() -> None:
    """
    Demonstrate the effect of performance cache on the project
    """
    pcv = mock.PropertyMock(return_value=0xb5)
    pc = mock.PropertyMock(return_value=b'\x00\x01\x02\x03')
    type(mock_vbaproject).performance_cache_version = pcv
    type(mock_vbaproject).performance_cache = pc
    vba_project_view = ProjectView(mock_vbaproject)
    expected = b'\xCC\x61\xB5\x00\x00\x03\x00\x00\x01\x02\x03'
    assert vba_project_view.to_bytes() == expected
