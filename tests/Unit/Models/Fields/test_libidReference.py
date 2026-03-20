import uuid
import pytest
from ms_ovba.Models.Fields.libid_reference import LibidReference


@pytest.mark.parametrize(
    "guid, ver, lib, path, name, expected", [
        ('0002043000000000C000000000000046',
         "2.0", "0", r"C:\Windows\System32\stdole2.tlb",
         "OLE Automation",
         r"*\G{00020430-0000-0000-C000-000000000046}"
         r"#2.0#0#C:\Windows\System32\stdole2.tlb#OLE Automation"),
        ('00000000000000000000000000000000', "2.0", "0", "C:\\", "",
         r"*\G{00000000-0000-0000-0000-000000000000}#2.0#0#C:\#"),
        ('00000000000000000000000000000000', "2.0", "0", "", "",
         r"*\G{00000000-0000-0000-0000-000000000000}#2.0#0##")
    ])
def test_str(guid, ver, lib, path, name, expected) -> None:
    guid = uuid.UUID(guid)
    libid_ref = LibidReference(guid, ver, lib, path, name)
    assert str(libid_ref) == expected


def test_str_posix(guid, ver, lib, path, name, expected) -> None:
    guid = uuid.UUID('00000000000000000000000000000000')
    libid_ref = LibidReference(guid, "2.0", "0", "", "", False)
    expected = r"*\H{00000000-0000-0000-0000-000000000000}#2.0#0##"
    assert str(libid_ref) == expected


def test_posix() -> None:
    guid = uuid.UUID('0002043000000000C000000000000046')
    libid_ref = LibidReference(
        guid,
        "2.0",
        "0",
        "//usr/bin/stdole2.tlb",
        "OLE Automation"
    )
    expected = ("*\\H{00020430-0000-0000-C000-000000000046}"
                "#2.0#0#//usr/bin/stdole2.tlb#OLE Automation")
    assert str(libid_ref) == expected


@pytest.mark.parametrize(
    "data", [
        (br'*\G{00020430-0000-0000-C000-000000000046}'
         br'#2.0#0#C:\Windows\System32\stdole2.tlb#OLE Automation'),
        (br"*\G{00000000-0000-0000-0000-000000000000}#0.0#0##"),
        (br"*\G{00000000-0000-0000-0000-000000000000}#0.0#0#C:\#"),
        (br"*\G{00000000-0000-0000-0000-000000000000}#0.0#0##Foo")
    ])
def test_unpack(data: bytes) -> None:
    lib = LibidReference.unpack(data)
    assert str(lib).encode("ascii") == data


@pytest.mark.parametrize("data", [
    (br'*\A{00000000-0000-0000-0000-000000000000}#2.0#0#C:\#Test'),
    (br'+\G{00000000-0000-0000-0000-000000000000}#2.0#0#C:\#Test'),
    (br'*\G{00000000-0000-0000-0000-000000000000}#12345.0#0#C:\#Test'),
    (br'*\G{00000000-0000-0000-0000-000000000000}#1#0#C:\#Test'),
    (br'*\G{00000000-0000-0000-0000-000000000000}#2.0#M#C:\#Test')
])
def test_unpack_exception(data) -> None:
    with pytest.raises(Exception):
        LibidReference.unpack(data)
