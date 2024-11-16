import struct
import uuid
from ms_ovba_compression.ms_ovba import MsOvba
from ms_pcode_assembler.module_cache import ModuleCache
from vbaproject_compiler.vbaProject import VbaProject
from vbaproject_compiler.Views.dirStream import DirStream
from vbaproject_compiler.Models.Fields.libid_reference import LibidReference
from vbaproject_compiler.Models.Entities.doc_module import DocModule
from vbaproject_compiler.Models.Entities.std_module import StdModule
from vbaproject_compiler.Models.Entities.reference_record import (
    ReferenceRecord
)


def test_dirstream() -> None:
    '''
    The cache is not yet tested.
    '''
    module_cache = ModuleCache(0xB5, 0x08F3, signature=3)
    # Read the data from the demo file and decompress it.
    f = open('tests/blank/vbaProject.bin', 'rb')
    offset = 0x1EC0
    length = 0x0232
    f.seek(offset)
    container = f.read(length)
    ms_ovba = MsOvba()
    decompressed_stream = ms_ovba.decompress(container)

    # Create a project with the same attributes
    project = VbaProject()
    stream = DirStream(project)
    stream.include_compat()
    codepage = 0x04E4
    codepage_name = "cp" + str(codepage)
    guid = uuid.UUID('0002043000000000C000000000000046')
    libid_ref = LibidReference(
        guid,
        "2.0",
        "0",
        "C:\\Windows\\System32\\stdole2.tlb",
        "OLE Automation"
    )
    ole_reference = ReferenceRecord(codepage_name, "stdole", libid_ref)
    guid = uuid.UUID('2DF8D04C5BFA101BBDE500AA0044DE52')
    libid_ref2 = LibidReference(
        guid,
        "2.0",
        "0",
        "C:\\Program Files\\Common Files\\Microsoft Shared\\OFFICE16\\MSO.DLL",
        "Microsoft Office 16.0 Object Library"
    )
    office_reference = ReferenceRecord(codepage_name, "Office", libid_ref2)
    project.add_reference(ole_reference)
    project.add_reference(office_reference)
    project.set_project_cookie(0x08F3)

    indirect_table = ("02 80 FE FF FF FF FF FF 20 00 00 00 FF FF FF FF",
                      "30 00 00 00 02 01 FF FF 00 00 00 00 00 00 00 00",
                      "FF FF FF FF FF FF FF FF 00 00 00 00 2E 00 43 00",
                      "1D 00 00 00 25 00 00 00 FF FF FF FF 40 00 00 00")
    module_cache.indirect_table = bytes.fromhex(" ".join(indirect_table))
    object_table = ("02 00 53 4C FF FF FF FF 00 00 01 00 53 10 FF FF",
                    "FF FF 00 00 01 00 53 94 FF FF FF FF 00 00 00 00",
                    "02 3C FF FF FF FF 00 00")
    module_cache.object_table = bytes.fromhex(" ".join(object_table))
    module_cache.misc = [[-1, 0x18], 0xFF, 0, [1, "00000000"]]
    module_cache.header.data2 = 0x0123
    module_cache.header.data3 = 0x88
    module_cache.header.sata4 = 8
    this_workbook = DocModule("ThisWorkbook")
    this_workbook.set_cookie(0xB81C)
    module_cache.cookie = 0xB81C
    guid = uuid.UUID('0002081900000000C000000000000046')
    this_workbook.set_guid(guid)
    module_cache.guid = [guid]
    this_workbook.set_cache(module_cache.to_bytes())

    sheet1 = DocModule("Sheet1")
    sheet1.set_cookie(0x9B9A)
    module_cache.cookie = 0x9B9A
    guid = uuid.UUID('0002082000000000C000000000000046')
    module_cache.guid = [guid]
    sheet1.set_guid(guid)
    sheet1.set_cache(module_cache.to_bytes())

    module1 = StdModule("Module1")
    module1.set_cookie(0xB241)
    module_cache.clear_variables()
    module_cache.cookie = 0xB241
    module_cache.misc = [[-1, 2], 0xFFFF, 0, [0, "FFFFFFFF"]]
    module_cache.header.data2 = 3
    module_cache.header.data3 = 0
    module_cache.header.sata4 = 7
    module_cache.indirect_table = struct.pack("<iI", -1, 0x78)
    module1.set_cache(module_cache.to_bytes())

    project.add_module(this_workbook)
    project.add_module(sheet1)
    project.add_module(module1)

    assert stream.to_bytes() == decompressed_stream

    # The OEM and 3rd party compression results are not the same,
    # so we compare the uncompressed streams.
    compressed = ms_ovba.compress(stream.to_bytes())
    assert ms_ovba.decompress(compressed) == decompressed_stream
