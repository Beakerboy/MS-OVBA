import pytest
from unittest import mock
from ms_ovba.Models.Entities.reference_original import ReferenceOriginal


mock_libid = mock.MagicMock()
mock_libid.__len__.return_value = 0x31
mock_libid.__str__.return_value = (
    r'*\G{00000000-0000-0000-0000-000000000000}#0.0#0##'
)


mock_refcntl = mock.Mock()
mock_refcntl.pack.return_value = (
    b'/\x00;\x00\x00\x001\x00\x00\x00'
    br'*\G{00000000-0000-0000-0000-000000000000}#0.0#0##'
    b'\x00\x00\x00\x00\x00\x000\x00O\x00\x00\x001\x00\x00\x00'
    br'*\G{00000000-0000-0000-0000-000000000000}#0.0#0##'
    b'\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x01\x00\x00\x00'
)


def test_constructor() -> None:
    module = ReferenceOriginal(mock_libid, mock_refcntl)
    assert isinstance(module, ReferenceOriginal)


min_hex = (
    b'3\x001\x00\x00\x00'
    br'*\G{00000000-0000-0000-0000-000000000000}#0.0#0##'
    b'/\x00;\x00\x00\x001\x00\x00\x00'
    br'*\G{00000000-0000-0000-0000-000000000000}#0.0#0##'
    b'\x00\x00\x00\x00\x00\x000\x00O\x00\x00\x001\x00\x00\x00'
    br'*\G{00000000-0000-0000-0000-000000000000}#0.0#0##'
    b'\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x01\x00\x00\x00'
)


def test_pack() -> None:
    codepage = 0x04E4
    cp_name = "cp" + str(codepage)
    ref_reg = ReferenceOriginal(mock_libid, mock_refcntl)
    results = ref_reg.pack('little', cp_name)
    assert results == min_hex


def test_unpack() -> None:
    codepage = 0x04E4
    cp_name = "cp" + str(codepage)
    base_path = 'ms_ovba.Models.Entities.reference_original.'
    path = base_path + 'LibidReference.unpack'
    with mock.patch(path) as mock_unpack:
        mock_unpack.return_value = mock_libid
        path1 = base_path + 'ReferenceControl.unpack'
        with mock.patch(path1) as mock_ctrl_unpack:
            mock_ctrl_unpack.return_value = mock_refcntl
            ref = ReferenceOriginal.unpack(min_hex, 'little')
            assert ref.pack('little', cp_name) == min_hex


def test_bad_id():
    min_hex = (
        b'4\x001\x00\x00\x00'
        br'*\G{00000000-0000-0000-0000-000000000000}#0.0#0##'
        b'/\x00;\x00\x00\x001\x00\x00\x00'
        br'*\G{00000000-0000-0000-0000-000000000000}#0.0#0##'
        b'\x00\x00\x00\x00\x00\x000\x00O\x00\x00\x001\x00\x00\x00'
        br'*\G{00000000-0000-0000-0000-000000000000}#0.0#0##'
        b'\x00\x00\x00\x00\x00\x00'
        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        b'\x01\x00\x00\x00'
    )
    with pytest.raises(Exception):
        ReferenceOriginal.unpack(min_hex, "little")
