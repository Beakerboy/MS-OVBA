import pytest
from ms_ovba.vbaProject import VbaProject


def test_set_get_default_date() -> None:
    project = VbaProject()
    date = project.default_date
    project.default_date = date
    assert project.default_date == date


def test_set_get_project_id() -> None:
    project = VbaProject()
    project.project_id = '{test}'
    assert project.project_id == '{test}'


def test_set_get_visibility() -> None:
    project = VbaProject()
    project.visibility_state = 0
    assert project.visibility_state == 0


def test_set_get_protection() -> None:
    project = VbaProject()
    project.protection_state = 0
    assert project.protection_state == 0


def test_set_get_visibility() -> None:
    project = VbaProject()
    project.visibility_state = 0
    assert project.visibility_state == 0


def test_set_get_password() -> None:
    project = VbaProject()
    project.password = 0
    assert project.password == 0


def test_set_get_cache() -> None:
    project = VbaProject()
    project.performance_cache = b'0'
    assert project.performance_cache == b'0'


def test_set_get_cache_version() -> None:
    project = VbaProject()
    project.performance_cache_version = 0x01
    assert project.performance_cache_version == 1


def test_set_get_codepage() -> None:
    project = VbaProject()
    project.codepage_name = 'cp1253'
    assert project.codepage_name == 'cp1252'


def test_set_get_cookie() -> None:
    project = VbaProject()
    project.project_cookie = 0x02
    assert project.project_cookie == 2


def test_bad_visibility() -> None:
    """
    Visibility must be zero or 0xFF
    """
    project = VbaProject()
    with pytest.raises(Exception):
        project.visibility_state = 1
