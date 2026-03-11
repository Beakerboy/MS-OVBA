import pytest
from ms_ovba.vbaProject import VbaProject


def test_set_get_visibility() -> None:
    project = VbaProject()
    project.visibility_state = 0
    assert project.visibility_state == 0


def test_set_get_protection() -> None:
    project = VbaProject()
    project.protection_state = 0
    assert project.protection_state == 0


def test_set_get_password() -> None:
    project = VbaProject()
    project.password = 0
    assert project.password == 0


def test_bad_visibility() -> None:
    """
    Visibility must be zero or 0xFF
    """
    project = VbaProject()
    with pytest.raises(Exception):
        project.visibility_state = 1
