import os
import pytest
import struct
import unittest.mock
import uuid
from ms_dtyp.filetime import Filetime
from ms_ovba_compression.ms_ovba import MsOvba
from ms_pcode_assembler.module_cache import ModuleCache
from ms_ovba.vbaProject import VbaProject
from ms_ovba.Models.Entities.doc_module import DocModule
from ms_ovba.Models.Entities.std_module import StdModule
from ms_ovba.Models.Entities.reference import (
    Reference
)
from ms_ovba.Models.Entities.reference_registered import (
    ReferenceRegistered
)
from ms_ovba.Models.Fields.libid_reference import LibidReference
from ms_ovba.Views.project_ole_file import ProjectOleFile
from ms_ovba.Views.project_view import ProjectView
from ms_ovba.Views.projectWm import ProjectWm
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
    root = "src/ms_ovba/blank_files/"
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
    libid_ref = ReferenceRegistered(LibidReference(
        uuid.UUID("0002043000000000C000000000000046"),
        "2.0",
        "0",
        "C:\\Windows\\System32\\stdole2.tlb",
        "OLE Automation"
    ))
    ole_reference = Reference(libid_ref, "stdole")
    libid_ref2 = ReferenceRegistered(LibidReference(
        uuid.UUID("2DF8D04C5BFA101BBDE500AA0044DE52"),
        "2.0",
        "0",
        "C:\\Program Files\\Common Files\\Microsoft Shared\\OFFICE16\\MSO.DLL",
        "Microsoft Office 16.0 Object Library"
    ))
    office_reference = Reference(libid_ref2, "Office")
    project.add_reference(ole_reference)
    project.add_reference(office_reference)
    proj_cookie = 0x08F3
    project.set_project_cookie(proj_cookie)
    project.set_project_id('{9E394C0B-697E-4AEE-9FA6-446F51FB30DC}')
    project.set_performance_cache(create_cache(proj_cookie))
    project.set_performance_cache_version(0x00B5)

    base_path = "src/ms_ovba/blank_files/"
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
    module_cache = ModuleCache(0xB5, proj_cookie, signature=3)
    module_cache.header.data2 = 3
    module_cache.header.data4 = 2
    module_cache.misc = [[-1, 0], 0xFFFF, 0, [0, "FFFFFFFF"]]
    module_cache.indirect_table = struct.pack("<iI", -1, 0x78)
    module_cache.module_cookie = cookie
    module1.add_workspace(26, 26, 1349, 522, 'Z')
    module_path = "tests/blank/Module1.bas"
    module1.add_file(module_path)
    module1.normalize_file()
    module1.set_cache(module_cache.to_bytes())

    project.add_module(this_workbook)
    project.add_module(sheet1)
    project.add_module(module1)

    # Check ProjectWm
    wm_bytes = ProjectWm(project).to_bytes()
    # Read from file instead of pasting
    expected = (b'ThisWorkbook\x00T\x00h' +
                b'\x00i\x00s\x00W\x00o\x00r\x00k\x00b\x00o' +
                b'\x00o\x00k\x00\x00\x00Sheet1\x00S\x00' +
                b'h\x00e\x00e\x00t\x001\x00\x00\x00Modu' +
                b'le1\x00M\x00o\x00d\x00u\x00l\x00e\x00' +
                b'1\x00\x00\x00\x00\x00')
    assert len(wm_bytes) == 0x56
    assert wm_bytes == expected

    # Check Project

    # Check Dir

    # Check _VBA_Project
    pv_bytes = ProjectView(project).to_bytes()
    bin_path = "tests/blank/vbaProject.bin"
    bin_offset = 0x14C0
    cache_size = 0x09F0
    b = open(bin_path, "rb")
    b.seek(bin_offset)
    file_bytes = b.read(cache_size)
    assert pv_bytes == file_bytes
    # assert len(pv_bytes) == 0x09F0

    ProjectOleFile.write_file(project)

    # combine sectors from bin into the streams
    # compare raw or uncompressed streams.


def create_cache(proj_cookie: int) -> bytes:
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
    libraries.append(LibidReference(
        uuid.UUID("000204EF-0000-0000-C000-000000000046"),
        "4.2",
        "9",
        "C:\\Program Files\\Common Files\\Microsoft Shared\\VBA"
        "\\VBA7.1\\VBE7.DLL",
        "Visual Basic For Applications"
    ))
    libraries.append(LibidReference(
        uuid.UUID("00020813-0000-0000-C000-000000000046"),
        "1.9",
        "0",
        "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE",
        "Microsoft Excel 16.0 Object Library"
    ))
    libraries.append(LibidReference(
        uuid.UUID("00020430-0000-0000-C000-000000000046"),
        "2.0",
        "0",
        "C:\\Windows\\System32\\stdole2.tlb",
        "OLE Automation"
    ))
    libraries.append(LibidReference(
        uuid.UUID("2DF8D04C-5BFA-101B-BDE5-00AA0044DE52"),
        "2.8",
        "0",
        "C:\\Program Files\\Common Files\\Microsoft Shared\\OFFICE16\\MSO.DLL",
        "Microsoft Office 16.0 Object Library"
    ))
    ca = struct.pack("<BIIHHIIH", 0xFF, 1033, 1033, 0x04E4, 3, 0, 0, 1)
    ca += struct.pack("<HH", len(libraries), 2)

    for lib in libraries:
        lib_str = bytearray(str(lib), "utf_16_le")
        ca += struct.pack("<H", len(lib_str))
        ca += lib_str
        ca += struct.pack("<III", 0, 0, 0)

    # User Class
    ca += struct.pack("<5H", 3, 2, 2, 1, 6)

    # Compile Time Data
    ca += struct.pack("<6IH", 0x0212,  0x010214, 0x010216, 0x0218,
                      0x01021a, 0x01021c, 0x0222)

    # Data
    ca += b'\xFF' * 6 + b'\x00' * 4 + b'\xFF' * 2 + b'\x00' * 2
    ca += struct.pack("<IH", 0x65BE0257, 0x11)

    # 64 bytes?
    ca += b'\xFF' * 8
    ca += struct.pack("<I", 1)
    ca += b'\xFF' * 36 + struct.pack("<H", 2) + b'\xFF' * 14

    # Footer?
    ca += struct.pack("<5IH", 1, 0, 0, 0, 0, proj_cookie)

    # Modules
    ca += struct.pack("<H", len(modules))
    i = 0

    data_str = ["57", "57", "63"]
    data = [0x0227, 0x022B, 0x022C]
    # data1 = i*24
    data1 = [0, 0x18, 0x30]
    data2 = [0x0333, 0x0333, 0x0283]
    for module in modules:
        name = module.modName.value.encode("utf_16_le")
        ca += struct.pack("<H", len(name)) + name
        txt = ("2" + chr(70 + i) + "65be02" + data_str[i]).encode("utf_16_le")
        ca += struct.pack("<H", len(txt)) + txt
        ca += struct.pack("<HHH", 0xFFFF, data[i], len(name)) + name
        ca += struct.pack("<HHIH", 0xFFFF, module.cookie.value, 0, 0)
        ca += struct.pack("<BIIH", data1[i], 2, data2[i], 0xFFFF)
        i += 1

    ca += struct.pack("<IH", 0xFFFFFFFF, 0x0101)
    neg_one_4b = b'\xFF\xFF\xFF\xFF'
    neg_one_one = neg_one_4b + struct.pack("<I", 1)
    bin_array = [
        b'\xf1q\x9a\xee\xc0\xe0\xc4F\xa2\xf8l|\xf9{s\x06',
        b'vS\x9e\xe1B\x85\xfeF\xa1\x8b0E\x08tCU',
        b'"\x93\xba>\xc3\x82\xfcD\x88\xcav\x96\xe5\x061"'
    ]

    record = (neg_one_4b * 13 + struct.pack("<2I", 0x0230, 0x0218) +
              neg_one_4b * 28 + struct.pack("<I", 0x0200) + neg_one_4b * 84)
    for byte_string in bin_array:
        record += byte_string + neg_one_one

    record += neg_one_4b + struct.pack("<I", 0x30)
    ca += struct.pack("<I", len(record)) + record
    names = [
        "Excel", "VBA", "Win16", "Win32", "Win64", "Mac", "VBA6", "VBA7",
        "Project1", "stdole", "VBAProject", "Office", "ThisWorkbook",
        "Evaluate", "Sheet1", "Module1", "Workbook"
        ]
    for name in names:
        ca += struct.pack("<HI" + str(len(name)) + "s", 0x2ba0,
                          0x04050000, name)
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
    module_cache = ModuleCache(cache_ver, proj_cookie, signature=3)
    module_cache.header.data3 = 0x88
    module_cache.header.data4 = 8
    module_cache.misc = [[-1, 0x18], 0x18, 0, [1, "00000000"]]
    indirect_table = ("02 80 FE FF FF FF FF FF 20 00 00 00 FF FF FF FF",
                      "30 00 00 00 02 01 FF FF 00 00 00 00 00 00 00 00",
                      "FF FF FF FF FF FF FF FF 00 00 00 00 2E 00 43 00",
                      "1D 00 00 00 25 00 00 00 FF FF FF FF 40 00 00 00")
    module_cache.indirect_table = bytes.fromhex(" ".join(indirect_table))

    object_table = [[2, 0x4C53], [1, 0x1053], [1, 0x9453], [0, 0x3C02]]
    object_table_bytes = b''
    for entry in object_table:
        object_table_bytes += struct.pack("<HHiH", *entry, -1, 0)
    module_cache.object_table = object_table_bytes

    module_cache.guid = [guid]
    module_cache.module_cookie = cookie

    mod.set_cache(module_cache.to_bytes())
    return mod
