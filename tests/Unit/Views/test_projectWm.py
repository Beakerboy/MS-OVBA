from ms_ovba.Views.projectWm import ProjectWm
from unittest import mock


mock_obj1 = mock.Mock()
mock_obj1.modName.value = "ThisWorkbook"
mock_obj2 = mock.Mock()
mock_obj2.modName.value = "Sheet1"
mock_obj3 = mock.Mock()
mock_obj3.modName.value = "Module1"
mock_vbaproject = mock.Mock()
mock_vbaproject.codepage_name = 'cp1252'
mock_vbaproject.modules = [mock_obj1, mock_obj2, mock_obj3]


def test_project_wm() -> None:
    project_wm = ProjectWm(mock_vbaproject)

    expected = (b'ThisWorkbook\x00T\x00h\x00i\x00s\x00W\x00o\x00r\x00k\x00b'
                + b'\x00o\x00o\x00k\x00\x00\x00Sheet1\x00S\x00h\x00e\x00e\x00'
                + b't\x001\x00\x00\x00Module1\x00M\x00o\x00d\x00u\x00l\x00e'
                + b'\x001\x00\x00\x00\x00\x00')
    result = project_wm.to_bytes()
    assert len(result) == 86
    assert result == expected
