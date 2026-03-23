import pytest
from ms_ovba.vbaProject import VbaProject


project: VbaProject


@pytest.fixture(autouse=True)
def run_around_tests() -> None:
    project = VbaProject()
    yield


def test_set_get_default_date() -> None:
    date = project.default_date
    project.default_date = date
    assert project.default_date == date


def test_set_get_project_id() -> None:
    project.project_id = '{test}'
    assert project.project_id == '{test}'


def test_set_get_visibility() -> None:
    project.make_visible()
    assert project.visibility_state == b'\xff'


def test_set_get_invisibility() -> None:
    project.make_invisible()
    assert project.visibility_state == b'\x00'


def test_get_protection() -> None:
    assert project.protection_state == b'\00' * 4


def test_set_user_protection() -> None:
    project.user_protect()
    expected = b'\x80\x00\x00\x00'
    assert project.protection_state == expected


def test_set_host_protection() -> None:
    project.host_protect()
    expected = b'\x40\x00\x00\x00'
    assert project.protection_state == expected


def test_set_vbe_protection() -> None:
    project.vbe_protect()
    expected = b'\x20\x00\x00\x00'
    assert project.protection_state == expected


def test_unset_protection() -> None:
    project.user_protect()
    project.host_protect()
    project.vbe_protect()
    expected = b'\xe0\x00\x00\x00'
    assert project.protection_state == expected
    project.user_unprotect()
    project.host_unprotect()
    project.vbe_unprotect()
    expected = b'\x00\x00\x00\x00'
    assert project.protection_state == expected


def test_set_get_password() -> None:
    project.password = 0
    assert project.password == 0


def test_set_get_cache() -> None:
    project.performance_cache = b'0'
    assert project.performance_cache == b'0'


def test_set_get_cache_version() -> None:
    project.performance_cache_version = 0x01
    assert project.performance_cache_version == 1


def test_set_get_codepage() -> None:
    project.codepage_name = 'cp1253'
    assert project.codepage_name == 'cp1253'


def test_set_get_cookie() -> None:
    project.project_cookie = 0x02
    assert project.project_cookie == 2


def test_include_projectwm() -> None:
    project.include_projectwm()
    assert project.projectwm


def test_exclude_projectwm() -> None:
    project.exclude_projectwm()
    assert not project.projectwm


def test_compat() -> None:
    project.include_compat()
    assert project._compat == True
    project.exclude_compat()
    assert project._compat == False
