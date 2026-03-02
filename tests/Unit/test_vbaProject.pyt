import pytest
from ms_ovba.vbaProject import VbaProject


def test_set_get_visibility() -> None:
    project = VbaProject()
    project.set_visibility_state(0)
    assert project.get_visibility_state() == 0


def test_set_get_protection() -> None:
    project = VbaProject()
    project.set_protection_state(0)
    assert project.get_protection_state() == 0


def test_set_get_password() -> None:
    project = VbaProject()
    project.set_password(0)
    assert project.get_password() == 0


def test_bad_visibility() -> None:
    """
    Visibility must be zero or 0xFF
    """
    project = VbaProject()
    with pytest.raises(Exception):
        project.set_visibility_state(1)
