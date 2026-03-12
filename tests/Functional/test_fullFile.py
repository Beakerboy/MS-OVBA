import os
import pytest
import struct
import unittest.mock
import uuid
from ms_dtyp.filetime import Filetime
from ms_ovba_compression.ms_ovba import MsOvba
from ms_pcode_assembler.module_cache import ModuleCache
from ms_pcode_assembler.project_cache import ProjectCache
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


def assert_module_matches_bin(module_path: str,
                       cache_size: int,
                       bin_path: str,
                       bin_offset: int,
                       bin_length: int) -> bool:
    m = open(module_path, "rb")
    b = open(bin_path, "rb")
    b.seek(bin_offset)
    assert m.read(cache_size) == b.read(cache_size)
    ms_ovba = MsOvba()
    m_uncompressed = ms_ovba.decompress(m.read())
    b_uncompressed = ms_ovba.decompress(b.read(bin_length))
    assert m_uncompressed == b_uncompressed


stdole_lib = LibidReference(
        uuid.UUID("00020430-0000-0000-C000-000000000046"),
        "2.0",
        "0",
        "C:\\Windows\\System32\\stdole2.tlb",
        "OLE Automation"
    )


@unittest.mock.patch('random.randint', NotSoRandom.randint)
def test_full_file() -> None:
    """
    Create an exact reproduction of a complete "empty" vba excel addin.
    """
    rand = [0x41, 0xBC, 0x7B, 0x7B, 0x37, 0x7B, 0x7B, 0x7B]
    NotSoRandom.set_seed(rand)
    project = VbaProject()
    project.default_date = Filetime.from_msfiletime(0x01D92433C2B823C0)
    project.include_projectwm()
    libid_ref = ReferenceRegistered(stdole_lib)
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
    project.project_cookie = proj_cookie
    project.project_id = '{9E394C0B-697E-4AEE-9FA6-446F51FB30DC}'
    project.performance_cache_version = 0x00B5

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
    module1.cookie = cookie
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
    module1.cache = module_cache.to_bytes()

    project.add_module(this_workbook)
    project.add_module(sheet1)
    project.add_module(module1)

    project.performance_cache = create_cache(
        proj_cookie,
        [this_workbook, sheet1, module1]
    )

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

    bin_offset = 0x14C0
    cache_size = 0x09F0
    bin_path = "tests/blank/vbaProject.bin"
    b = open(bin_path, "rb")
    b.seek(bin_offset)
    file_bytes = b.read(cache_size)
    assert pv_bytes == file_bytes
    assert len(pv_bytes) == 0x09F0

    ProjectOleFile.write_file(project)

    # Check Modules

    path = "tests/blank/Module1.bas"
    cache_size = 0x333
    bin_path = "vbaProject.bin"
    bin_offset = 0x1200
    bin_length = 0x2a9
    assert_module_matches_bin(
        path, cache_size, bin_path,
        bin_offset, bin_length
    )

    # combine sectors from bin into the streams
    # compare raw or uncompressed streams.


def create_cache(proj_cookie: int, modules) -> bytes:
    cache = ProjectCache(0x04E4, proj_cookie, 0x65BE0257)
    cache._hex = 0x65BE0257
    module_array = []
    i = 0
    id = [0x227, 0x22B, 0x22C]
    for module in modules:
        hex = 0x65BE0263 if i == 2 else cache._hex
        module_array.append(
            (module.name, 50, 70 + i, hex, id[i],
             module.cookie, len(module.cache), [], -1)
        )
        i += 1

    cache._modules = module_array

    cache.add_library(str(LibidReference(
        uuid.UUID("000204EF-0000-0000-C000-000000000046"),
        "4.2",
        "9",
        "C:\\Program Files\\Common Files\\Microsoft Shared\\VBA"
        "\\VBA7.1\\VBE7.DLL",
        "Visual Basic For Applications"
    )))
    cache.add_library(str(LibidReference(
        uuid.UUID("00020813-0000-0000-C000-000000000046"),
        "1.9",
        "0",
        "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE",
        "Microsoft Excel 16.0 Object Library"
    )))
    cache.add_library(str(stdole_lib))
    cache.add_library(str(LibidReference(
        uuid.UUID("2DF8D04C-5BFA-101B-BDE5-00AA0044DE52"),
        "2.8",
        "0",
        "C:\\Program Files\\Common Files\\Microsoft Shared\\OFFICE16\\MSO.DLL",
        "Microsoft Office 16.0 Object Library"
    )))

    # User Class
    cache._user = [2, 2, 1]

    # Compile Time Data
    cache._compile = [0x0212, 0x010214, 0x010216,
                      0x0218, 0x01021a, 0x01021c]

    # Data
    cache._data = [0x222, 0xffff, 17, -1, -1, -1, -1, 1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1]

    # Footer?
    cache._post_f_data = [(13, 0x230), (14, 0x218), (43, 0x200)]
    cache._post_data = [
        b'\xf1q\x9a\xee\xc0\xe0\xc4F\xa2\xf8l|\xf9{s\x06',
        b'vS\x9e\xe1B\x85\xfeF\xa1\x8b0E\x08tCU',
        b'"\x93\xba>\xc3\x82\xfcD\x88\xcav\x96\xe5\x061"'
    ]
    cache._post_footer = 0x30
    cache._w0 = 0x117
    cache._w2 = 0x2ba0
    cache._identifiers = [
        (b"Excel", 4, 0x2b80), (b"VBA", 4, 0xe2f7), (b"Win16", 4, 0x7ec1),
        (b"Win32", 4, 0x7f07), (b"Win64", 4, 0x7f78), (b"Mac", 4, 0xb2b3),
        (b"VBA6", 4, 0x23ad), (b"VBA7", 4, 0x23ae),
        (b"Project1", 4, 0x170a),
        (b"stdole", 4, 0x6093), (b"VBAProject", 4, 0xbfbe),
        (b"Office", 4, 0x7515), (b"ThisWorkbook", 4, 0xe37c),
        (b"_Evaluate", 128, 0xd918, 0, 0x103, -1),
        (b"Sheet1", 4, 0x1ae8), (b"Module1", 4, 0x1162),
        (b"Workbook", 4, 0x186b)
    ]

    hex = ("20 02 02 00 FF FF 22 02 FF FF FF FF 24 02 03 00",
           "FF FF 27 02 00 00 03 00 FF FF FF FF FF FF 2B 02",
           "01 00 03 00 2D 02 02 00 05 00 0E 02 01 00 FF FF",
           "10 02 00 00 FF FF FF FF FF FF FF FF FF FF FF FF",
           "FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF",
           "FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF")

    hex2 = ("06 00 10 00 00 00 01 00 36 00 00 00 00 00 00 00",
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
            "00 00")

    cache._footer = [
        bytes.fromhex(" ".join(hex)),
        bytes.fromhex(" ".join(hex2))
    ]
    return cache.to_bytes()


def create_doc_module(project: VbaProject, name: str,
                      cookie: int, guid_s: str, path: str) -> DocModule:
    mod = DocModule(name)
    mod.cookie = cookie
    guid = uuid.UUID(guid_s)
    mod.add_guid(guid)
    module_path = path
    mod.add_file(module_path)
    mod.normalize_file()

    cache_ver = project.performance_cache_version
    proj_cookie = project.project_cookie
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

    mod.cache = module_cache.to_bytes()
    return mod
