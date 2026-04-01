import unittest.mock
from ms_ovba.Views.project import Project
from typing import Type, TypeVar


T = TypeVar('T', bound='NotSoRandom')


class NotSoRandom():
    _rand = []

    @classmethod
    def set_seed(cls: Type[T], seeds: list) -> None:
        cls._rand = seeds

    @classmethod
    def randint(cls: Type[T], param1: int, param2: int) -> int:
        return cls._rand.pop(0)


class Obj:
    def __init__(self: T, name: str) -> None:
        self.value = name


class Mod:
    def __init__(self: T, name: str) -> None:
        self.modName = Obj(name)
        self.workspace = [0, 0, 0, 0, 'C']

    def to_project_module_string(self: T) -> str:
        return "Document" + "=" + self.modName.value + "/&H00000000"


class Mod1:
    def __init__(self: T, name: str) -> None:
        self.modName = Obj(name)
        self.workspace = [26, 26, 1349, 522, 'Z']

    def to_project_module_string(self: T) -> str:
        return "Module=Module1"


class MockVbaProject:
    def __init__(self: T) -> None:
        mod1 = Mod1("Module1")
        self.modules = [Mod("ThisWorkbook"),
                        Mod("Sheet1"), mod1]
        self.project_id = '{9E394C0B-697E-4AEE-9FA6-446F51FB30DC}'
        self.codepage_name = 'cp1252'
        self.protection_state = b'\x00\x00\x00\x00'
        self.password = b'\x00'
        self.visibility_state = b'\xFF'
        self.attributes = {}
        self.help_context_id = 0


@unittest.mock.patch('random.randint', NotSoRandom.randint)
def test_blank() -> None:
    rand = [0x41, 0xBC, 0x7B, 0x7B, 0x37, 0x7B, 0x7B, 0x7B]
    NotSoRandom.set_seed(rand)
    vba_project = MockVbaProject()
    project = Project(vba_project)
    project.add_attribute("VersionCompatible32", "393222000")

    project.hostExtenderInfo = ("&H00000001="
                                + "{3832D640-CF90-11CF-8E43-00A0C911005A};VBE;"
                                + "&H00000000")
    file = open("tests/blank/vbaProject.bin", "rb")
    file.seek(0x2180)
    expected = file.read(0x0080)
    file.seek(0x2400)
    expected += file.read(0x0152)

    assert project.to_bytes() == expected


def test_guid_valid() -> None:
    guid = "{9E394C0B-697E-4AEE-9FA6-446F51FB30DC}"
    assert Project._valid_guid(guid)


def test_guid_invalid() -> None:
    guid = "{9E394C0Z-697E-4AEE-9FA6-446F51FB30DC}"
    assert not Project._valid_guid(guid)


def test_project_line_valid() -> None:
    line = 'ID="{9E394C0B-697E-4AEE-9FA6-446F51FB30DC}"'
    assert Project._valid_project_id_line(line)


def test_password_line_valid() -> None:
    line = 'DPB="BCBEA7A2591C5A1C5A1C"'
    assert Project._valid_password_line(line)


def test_project_line_invalid() -> None:
    line = 'ID={9E394C0B-697E-4AEE-9FA6-446F51FB30DC}'
    assert not Project._valid_project_id_line(line)


def test_host_extender_line() -> None:
    line = "&H00000001={3832D640-CF90-11CF-8E43-00A0C911005A};VBE;&H00000000"
    assert Project._valid_host_extender_line(line)


def test_valid() -> None:
    path = 'tests/blank/PROJECT'
    assert Project.is_valid(path)


def test_incorrect_line_endings() -> None:
    path = 'tests/test_files/PROJECT_bad'
    assert not Project.is_valid(path)
