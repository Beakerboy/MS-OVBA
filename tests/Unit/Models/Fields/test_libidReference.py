import uuid
import pytest
from ms_ovba.Models.Fields.libid_reference import LibidReference


def test_str() -> None:
    guid = uuid.UUID('0002043000000000C000000000000046')
    libid_ref = LibidReference(
        guid,
        "2.0",
        "0",
        "C:\\Windows\\System32\\stdole2.tlb",
        "OLE Automation"
    )
    expected = ("*\\G{00020430-0000-0000-C000-000000000046}"
                "#2.0#0#C:\\Windows\\System32\\stdole2.tlb#OLE Automation")
    assert str(libid_ref) == expected
    assert len(libid_ref) == 94


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


def test_unpack() -> None:
    data = (b'*\\G{00020430-0000-0000-C000-000000000046}'
            b'#2.0#0#C:\\Windows\\System32\\stdole2.tlb#OLE Automation')
    lib = LibidReference.unpack(data)
    assert lib._version == "2.0"


def test_unpack_exception() -> None:
    data = (b'*\\A{00020430-0000-0000-C000-000000000046}'
            b'#2.0#0#C:\\Windows\\System32\\stdole2.tlb#OLE Automation')
    with pytest.raises(Exception):
        lib = LibidReference.unpack(data)
