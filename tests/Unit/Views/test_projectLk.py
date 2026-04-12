from ms_ovba.Views.projectLk import ProjectLk
from unittest import mock


mock_vbaproject = mock.Mock()


mock_license = mock.Mock()
mock_license.to_bytes.return_value = b'Test'


def test_project_lk_empty() -> None:
    mock_vbaproject._license_records = []
    project_lk = ProjectLk(mock_vbaproject)

    expected = (b'\x01\x00\x00\x00\x00\x00')
    result = project_lk.to_bytes()
    assert result == expected


def test_project_lk() -> None:
    mock_vbaproject._license_records = [mock_license]
    project_lk = ProjectLk(mock_vbaproject)

    expected = (b'\x01\x00\x01\x00\x00\x00Test')
    result = project_lk.to_bytes()
    assert result == expected
