from ms_ovba.Views.dirStream import DirStream
from typing import TypeVar
from unittest import mock


mock_vbaproject = mock.Mock()


def test_construct() -> None:
    dir = DirStream(mock_vbaproject)
    assert isinstance(dir, DirStream)
