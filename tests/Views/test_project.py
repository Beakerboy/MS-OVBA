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
    def __init__(self, name) -> None:
        self.value = name


class Mod:
    def __init__(self, name, type) -> None:
        self.modName = Obj(name)
        self.workspace = [0, 0, 0, 0, 'C']
        self.type = type

    def to_project_module_string(self):
        return self.type + "=" + self.modName.value


class MockVbaProject:
    def __init__(self) -> None:
        mod1 = Mod("Module1", "Module")
        mod1.workspace = [26, 26, 1349, 522, 'Z']
        self.modules = [Mod("ThisWorkbook", "Document"), Mod("Sheet1", "Document"), mod1]
        self.project_id = '{9E394C0B-697E-4AEE-9FA6-446F51FB30DC}'

    def get_codepage_name(self):
        return 'cp1252'

    def get_project_id(self):
        return self.project_id

    def get_protection_state(self):
        return b'\x00\x00\x00\x00'

    def get_password(self):
        return b'\x00'

    def get_visibility_state(self):
        return b'\xFF'


@unittest.mock.patch('random.randint', NotSoRandom.randint)
def test_blank() -> None:
    rand = [0x41, 0xBC, 0x7B, 0x7B, 0x37, 0x7B, 0x7B, 0x7B]
    NotSoRandom.set_seed(rand)
    vba_project = MockVbaProject()
    project = Project(vba_project)
    project.add_attribute("HelpContextID", "0")
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
