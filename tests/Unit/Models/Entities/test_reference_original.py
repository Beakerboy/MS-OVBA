import pytest
from unittest import mock
from ms_ovba.Models.Entities.reference_original import ReferenceOriginal


class MockLibid:
    def __len__(self) -> int:
        return 0x31

    def __str__(self) -> str:
        return (r'*\G{00000000-0000-0000-0000-000000000000}#0.0#0##')


class MockRefCntl:
    def pack(self, endien, name) -> bytes:
        return (
            b'/\x00;\x00\x00\x001\x00\x00\x00'
            br'*\G{00000000-0000-0000-0000-000000000000}#0.0#0##'
            b'\x00\x00\x00\x00\x00\x00O\x00\x00\x001\x00\x00\x00'
            br'*\G{00000000-0000-0000-0000-000000000000}#0.0#0##'
            b'\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            b'\x01\x00\x00\x00'
        )

    def unpack(self, endien):
        return MockRefCntl()


def test_constructor() -> None:
    lib = MockLibid()
    ref = MockRefCntl()
    module = ReferenceOriginal(lib, ref)
    assert isinstance(module, ReferenceOriginal)


min_hex = (
    b'3\x001\x00\x00\x00'
    br'*\G{00000000-0000-0000-0000-000000000000}#0.0#0##'
    b'/\x00;\x00\x00\x001\x00\x00\x00'
    br'*\G{00000000-0000-0000-0000-000000000000}#0.0#0##'
    b'\x00\x00\x00\x00\x00\x00O\x00\x00\x001\x00\x00\x00'
    br'*\G{00000000-0000-0000-0000-000000000000}#0.0#0##'
    b'\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x01\x00\x00\x00'
)


def test_pack() -> None:
    codepage = 0x04E4
    cp_name = "cp" + str(codepage)
    ref_reg = ReferenceOriginal(MockLibid(), MockRefCntl())
    results = ref_reg.pack('little', cp_name)
    assert results == min_hex


def test_unpack() -> None:
    codepage = 0x04E4
    cp_name = "cp" + str(codepage)
    ref = ReferenceOriginal.unpack(min_hex, 'little')
    assert ref.pack('little', cp_name) == min_hex


def test_bad_id():
    path = 'ms_ovba.Models.Entities.reference_original.LibidReference'
    with mock.patch(path, MockLibid):
        path1 = 'ms_ovba.Models.Entities.reference_original.ReferenceControl'
        with mock.patch(path1, MockLibid):
            with pytest.raises(Exception):
                ReferenceOriginal.unpack(min_hex, "little")
