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
    project.make_visible()
    assert project.visibility_state == b'\xff'


def test_set_get_invisibility() -> None:
    project = VbaProject()
    project.make_invisible()
    assert project.visibility_state == b'\x00'


def test_get_protection() -> None:
    project = VbaProject()
    assert project.protection_state == b'\00' * 4


def test_get_protection() -> None:
    project = VbaProject()
    project.user_protect()
    expected = b'\x80\x00\x00\x00'
    assert project.protection_state == expected


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
    assert project.codepage_name == 'cp1253'


def test_set_get_cookie() -> None:
    project = VbaProject()
    project.project_cookie = 0x02
    assert project.project_cookie == 2


def test_include_projectwm() -> None:
    project = VbaProject()
    project.include_projectwm()
    assert project.projectwm


def test_exclude_projectwm() -> None:
    project = VbaProject()
    project.exclude_projectwm()
    assert not project.projectwm


def test_bad_visibility() -> None:
    """
    Visibility must be zero or 0xFF
    """
    project = VbaProject()
    with pytest.raises(Exception):
        project.visibility_state = 1
