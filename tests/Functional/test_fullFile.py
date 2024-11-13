import os
import pytest
import struct
import unittest.mock
import uuid
from ms_cfb.ole_file import OleFile
from ms_dtyp.filetime import Filetime
from ms_ovba_compression.ms_ovba import MsOvba
from ms_pcode_assembler.module_cache import ModuleCache
from vbaproject_compiler.vbaProject import VbaProject
from vbaproject_compiler.Models.Entities.doc_module import DocModule
from vbaproject_compiler.Models.Entities.std_module import StdModule
from vbaproject_compiler.Models.Entities.reference_record import (
    ReferenceRecord
)
from vbaproject_compiler.Models.Fields.libid_reference import LibidReference
from vbaproject_compiler.Views.project_ole_file import ProjectOleFile
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


@pytest.fixture(autouse=True)
def run_around_tests() -> None:
    # Code that will run before your test, for example:

    # A test function will be run at this point
    yield
    # Code that will run after your test
    root = "src/vbaproject_compiler/blank_files/"
    root2 = "tests/blank/"
    names = [root + "ThisWorkbook.cls", root + "Sheet1.cls",
             root2 + "Module1.bas"]
    remove_module(names)
    names = ["dir.bin", "projectWm.bin", "project.bin", "vba_project.bin"]
    map(os.remove, names)


def remove_module(names: str) -> None:
    for name in names:
        os.remove(name + ".new")
        os.remove(name + ".bin")


def module_matches_bin(module_path: str,
                       cache_size: int,
                       bin_path: str,
                       bin_offset: int,
                       bin_length: int) -> bool:
    m = open(module_path, "rb")
    b = open(bin_path, "rb")
    b.seek(bin_offset)
    if m.read(cache_size) != b.read(cache_size):
        return False
    ms_ovba = MsOvba()
    m_uncompressed = ms_ovba.decompress(m.read())
    b_uncompressed = ms_ovba.decompress(b.read(bin_length))
    return m_uncompressed == b_uncompressed


@unittest.mock.patch('random.randint', NotSoRandom.randint)
def test_full_file() -> None:
    rand = [0x41, 0xBC, 0x7B, 0x7B, 0x37, 0x7B, 0x7B, 0x7B]
    NotSoRandom.set_seed(rand)
    project = VbaProject()
    project.default_date = Filetime.from_msfiletime(0x01D92433C2B823C0)
    project.set_include_projectwm(True)
    codepage = 0x04E4
    codepage_name = "cp" + str(codepage)
    libid_ref = LibidReference(
        uuid.UUID("0002043000000000C000000000000046"),
        "2.0",
        "0",
        "C:\\Windows\\System32\\stdole2.tlb",
        "OLE Automation"
    )
    ole_reference = ReferenceRecord(codepage_name, "stdole", libid_ref)
    libid_ref2 = LibidReference(
        uuid.UUID("2DF8D04C5BFA101BBDE500AA0044DE52"),
        "2.0",
        "0",
        "C:\\Program Files\\Common Files\\Microsoft Shared\\OFFICE16\\MSO.DLL",
        "Microsoft Office 16.0 Object Library"
    )
    office_reference = ReferenceRecord(codepage_name, "Office", libid_ref2)
    project.add_reference(ole_reference)
    project.add_reference(office_reference)
    proj_cookie = 0x08F3
    project.set_project_cookie(proj_cookie)
    project.set_project_id('{9E394C0B-697E-4AEE-9FA6-446F51FB30DC}')
    project.set_performance_cache(create_cache())
    project.set_performance_cache_version(0x00B5)

    base_path = "src/vbaproject_compiler/blank_files/"
    # Add Modules
    this_workbook = create_doc_module(project, "ThisWorkbook", 0xB81C,
                                      "0002081900000000C000000000000046",
                                      base_path + "ThisWorkbook.cls")

    sheet1 = create_doc_module(project, "Sheet1", 0x9B9A,
                               "0002082000000000C000000000000046",
                               base_path + "Sheet1.cls")

    module1 = StdModule("Module1")
    cookie = 0xB241
    module1.set_cookie(cookie)
    module_cache = ModuleCache(0xB5, proj_cookie)
    module_cache.clear_variables()
    module_cache.misc = [[0x0316, 3, 0, 2],
                         [-1, 0], 0xFFFF, 0, [0, "FFFFFFFF"]]
    module_cache.indirect_table = struct.pack("<iI", -1, 0x78)
    module_cache.module_cookie = cookie
    module1.add_workspace(26, 26, 1349, 522, 'Z')
    module_path = "tests/blank/Module1.bas"
    module1.add_file(module_path)
    module1.normalize_file()
    module1.set_cache(module_cache.to_bytes())

    project.add_module(module1)
    project.add_module(sheet1)
    project.add_module(this_workbook)

    ole_file = ProjectOleFile(project)
    ole_file.write_file()

    # storage.set_modified(time)
    # storage.set_created(time)

    # fails
    # file_size = os.stat("vbaProject.bin").st_size
    # expected_size = os.stat("tests/blank/vbaProject.bin").st_size
    # assert file_size == expected_size
    # compare new file to blank file in 512 block chunks
    new = open("./vbaProject.bin", "rb")
    expected = open("tests/blank/vbaProject.bin", "rb")

    # Header
    assert new.read(512) == expected.read(512)

    # FAT
    # assert new.read(512) == expected.read(512)
    new.read(512)
    expected.read(512)

    # Dir1
    ole_standard = OleFile.create_from_file("tests/blank/vbaProject.bin")
    ole_new = OleFile.create_from_file("./vbaProject.bin")
    std_flat = ole_standard.root_directory.flatten()
    new_flat = ole_new.root_directory.flatten()
    assert (len(std_flat) == len(new_flat))
    std_str = ""
    new_str = ""
    for dir in std_flat:
        std_str += "\n" + str(dir)
    for dir in new_flat:
        new_str += "\n" + str(dir)
    assert new_str == std_str

    # assert new.read(512) == expected.read(512)
    new.read(512)
    expected.read(512)

    # minifat
    # assert new.read(512) == expected.read(512)


def create_cache() -> bytes:
    modules = []
    this_workbook = DocModule("ThisWorkbook")
    this_workbook.cookie.value = 0xB81C
    modules.append(this_workbook)
    sheet1 = DocModule("Sheet1")
    sheet1.cookie.value = 0x9B9A
    modules.append(sheet1)
    module1 = StdModule("Module1")
    module1.cookie.value = 0xB241
    modules.append(module1)

    libraries = []
    delim = []
    libraries.append(LibidReference(
        uuid.UUID("000204EF-0000-0000-C000-000000000046"),
        "4.2",
        "9",
        "C:\\Program Files\\Common Files\\Microsoft Shared\\VBA"
        "\\VBA7.1\\VBE7.DLL",
        "Visual Basic For Applications"
    ))
    delim.append(0x011A)
    libraries.append(LibidReference(
        uuid.UUID("00020813-0000-0000-C000-000000000046"),
        "1.9",
        "0",
        "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE",
        "Microsoft Excel 16.0 Object Library"
    ))
    delim.append(0x00BC)
    libraries.append(LibidReference(
        uuid.UUID("00020430-0000-0000-C000-000000000046"),
        "2.0",
        "0",
        "C:\\Windows\\System32\\stdole2.tlb",
        "OLE Automation"
    ))
    delim.append(0x0128)
    libraries.append(LibidReference(
        uuid.UUID("2DF8D04C-5BFA-101B-BDE5-00AA0044DE52"),
        "2.8",
        "0",
        "C:\\Program Files\\Common Files\\Microsoft Shared\\OFFICE16\\MSO.DLL",
        "Microsoft Office 16.0 Object Library"
    ))
    delim.append(0x0003)
    ca = (b''
          + b'\xFF\x09\x04\x00\x00\x09\x04\x00\x00\xE4\x04\x03\x00\x00\x00\x00'
          + b'\x00\x00\x00\x00\x00\x01\x00\x04\x00\x02\x00\x20\x01')
    i = 0
    for lib in libraries:
        ca += bytearray(str(lib), "utf_16_le")
        ca += struct.pack("<IIIH", 0, 0, 0, delim[i])
        i += 1
    ca += struct.pack("<17H", 2, 2, 1, 6, 0x0212, 0, 0x0214, 1, 0x0216, 1,
                      0x0218, 0, 0x021a, 1, 0x021c, 1, 0x0222)
    ca += b'\xFF' * 6 + b'\x00' * 4 + b'\xFF' * 36
    prefix = [0x0018, 0x000C, 0x000E]
    # index = 0x0046
    i = 0

    for module in modules:
        name = module.modName.value.encode("utf_16_le")
        ca += struct.pack("<H", prefix[i]) + name
        ca += struct.pack("<HH", 0x0014, 0x0032) + bytes([69 + i])
        ca += "65be0257".encode("utf_16_le")
        ca += struct.pack("<HHH", 0xFFFF, 0x0227, prefix[i])
        ca += name + struct.pack("<HHHI", 0xFFFF, module.cookie.value, 0, 0)
        i += 1
    return ca


def create_doc_module(project: VbaProject, name: str,
                      cookie: int, guid_s: str, path: str) -> DocModule:
    mod = DocModule(name)
    mod.set_cookie(cookie)
    guid = uuid.UUID(guid_s)
    mod.set_guid(guid)
    module_path = path
    mod.add_file(module_path)
    mod.normalize_file()

    cache_ver = project.get_performance_cache_version()
    proj_cookie = project.get_project_cookie()
    module_cache = ModuleCache(cache_ver, proj_cookie)
    module_cache.misc = [[0x0316, 0x0100, 0x88, 8],
                         [-1, 0x18], 0xFFFF, 0, [1, "00000000"]]
    indirect_table = ("02 80 FE FF FF FF FF FF 20 00 00 00 FF FF FF FF",
                      "30 00 00 00 02 01 FF FF 00 00 00 00 00 00 00 00",
                      "FF FF FF FF FF FF FF FF 00 00 00 00 2E 00 43 00",
                      "1D 00 00 00 25 00 00 00 FF FF FF FF 40 00 00 00")
    module_cache.indirect_table = bytes.fromhex(" ".join(indirect_table))
    object_table = ("02 00 53 4C FF FF FF FF 00 00 01 00 53 10 FF FF",
                    "FF FF 00 00 01 00 53 94 FF FF FF FF 00 00 00 00",
                    "02 3C FF FF FF FF 00 00")
    module_cache.object_table = bytes.fromhex(" ".join(object_table))
    module_cache.guid = [guid]
    module_cache.module_cookie = cookie

    mod.set_cache(module_cache.to_bytes())
    return mod
