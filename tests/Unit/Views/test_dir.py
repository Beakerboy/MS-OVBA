import pytest
from pathlib import osPath
from ms_cfb.ole_file import OleFile
from ms_ovba.Views.dirStream import DirStream
from ms_ovba_compression.ms_ovba import MsOvba
from unittest import mock


mock_vbaproject = mock.Mock()


@pytest.fixture
def my_fixture():
    # Setup: Runs BEFORE the test
    # print("\nSetting up...")
    yield
    # Teardown: Runs AFTER the test
    osPath("tests/blank/dir.bin").unlink(missing_ok=True)


def test_construct() -> None:
    dir = DirStream(mock_vbaproject)
    assert isinstance(dir, DirStream)


def test_is_valid() -> None:
    file = "tests/blank/vbaProject.bin"
    ole_file = OleFile.create_from_file(file)
    ole_file.extract_stream('dir', 'tests/blank')
    with open('tests/blank/dir.bin', 'rb') as f:
        compressed_data = f.read()

        # Use MsOvba to decompress the stream
        ms_ovba = MsOvba()
        decompressed_data = ms_ovba.decompress(compressed_data)
        assert DirStream.is_valid(decompressed_data)


def test_from_bytes() -> None:
    expected = {}
    file = "tests/blank/vbaProject.bin"
    ole_file = OleFile.create_from_file(file)
    ole_file.extract_stream('dir', 'tests/blank')
    with open('tests/blank/dir.bin', 'rb') as f:
        compressed_data = f.read()

        # Use MsOvba to decompress the stream
        ms_ovba = MsOvba()
        decompressed_data = ms_ovba.decompress(compressed_data)
        assert DirStream.from_bytes(decompressed_data) == expected
