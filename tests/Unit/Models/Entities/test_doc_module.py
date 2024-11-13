import uuid
from ms_ovba_compression.ms_ovba import MsOvba
from ms_pcode_assembler.module_cache import ModuleCache
from vbaproject_compiler.Models.Entities.doc_module import DocModule


def test_normalize() -> None:

    cache = ModuleCache(0xB5, 0x08F3)
    cache.module_cookie = 0xB81C
    cache.misc = [[0x0316, 0, 0x0123, 0x88],
                  [-1, 8], 24, "00000000", 1, 0]
    guid = uuid.UUID('0002081900000000C000000000000046')
    cache.guid = [guid]

    indirect_table = ("02 80 FE FF FF FF FF FF 20 00 00 00 FF FF FF FF",
                      "30 00 00 00 02 01 FF FF 00 00 00 00 00 00 00 00",
                      "FF FF FF FF FF FF FF FF 00 00 00 00 2E 00 43 00",
                      "1D 00 00 00 25 00 00 00 FF FF FF FF 40 00 00 00")
    cache.indirect_table = bytes.fromhex(" ".join(indirect_table))
    object_table = ("02 00 53 4C FF FF FF FF 00 00 01 00 53 10 FF FF",
                    "FF FF 00 00 01 00 53 94 FF FF FF FF 00 00 00 00",
                    "02 3C FF FF FF FF 00 00")
    cache.object_table = bytes.fromhex(" ".join(object_table))

    module = DocModule("foo")
    path1 = "src/vbaproject_compiler/blank_files/ThisWorkbook.cls"
    module.add_file(path1)
    module.cookie.value = 0xB81C
    guid = uuid.UUID('0002081900000000C000000000000046')
    module.set_guid(guid)
    module.normalize_file()
    f = open(path1 + ".new", "rb")
    path2 = "tests/blank/ThisWorkbook"
    e = open(path2, "rb")
    assert f.read() == e.read()
    # while line := f.readline():
    #     assert line == e.readline()

    module.set_cache(cache.to_bytes())
    module.write_file()
    path3 = path1 + ".bin"
    f_stream = open(path3, "rb")
    full_binary = open('tests/blank/vbaProject.bin', 'rb')
    offset = 0x0800
    length1 = 0x0333
    length2 = 0x00B4
    full_binary.seek(offset)
    cache = full_binary.read(length1)
    assert f_stream.read(0x333) == cache

    container = full_binary.read(length2)
    ms_ovba = MsOvba()
    test_data = ms_ovba.decompress(f_stream.read())
    expected_data = ms_ovba.decompress(container)
    assert test_data == expected_data
