import pytest
from pathlib import Path
from ms_cfb.ole_file import OleFile
from ms_ovba.Views.dirStream import DirStream
from ms_ovba_compression.ms_ovba import MsOvba
from unittest import mock


mock_vbaproject = mock.Mock()


@pytest.fixture
def my_fixture() -> None:
    # Setup: Runs BEFORE the test
    # print("\nSetting up...")
    yield
    # Teardown: Runs AFTER the test
    Path("tests/blank/dir.bin").unlink(missing_ok=True)


def test_construct() -> None:
    dir = DirStream(mock_vbaproject)
    assert isinstance(dir, DirStream)


@pytest.mark.usefixtures("my_fixture")
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


@pytest.mark.usefixtures("my_fixture")
def test_from_bytes() -> None:
    expected = {
        'codepage_name': 'cp1252',
        'help_context_id': 0,
        'major_version': 1706951255,
        'minor_version': 17,
        'cookie': 2291,
        'modules': [{'cookie': 47132,
                'docstring': '',
                'help_context': 0,
                'name': 'ThisWorkbook',
                'offset': 819,
                'private': False,
                'read_only': False,
                'stream_name': 'ThisWorkbook',
                'type': 34},
               {'cookie': 39834,
                'docstring': '',
                'help_context': 0,
                'name': 'Sheet1',
                'offset': 819,
                'private': False,
                'read_only': False,
                'stream_name': 'Sheet1',
                'type': 34},
               {'cookie': 45633,
                'docstring': '',
                'help_context': 0,
                'name': 'Module1',
                'offset': 643,
                'private': False,
                'read_only': False,
                'stream_name': 'Module1',
                'type': 33}]
    }
    file = "tests/blank/vbaProject.bin"
    ole_file = OleFile.create_from_file(file)
    ole_file.extract_stream('dir', 'tests/blank')
    with open('tests/blank/dir.bin', 'rb') as f:
        compressed_data = f.read()

        # Use MsOvba to decompress the stream
        ms_ovba = MsOvba()
        decompressed_data = ms_ovba.decompress(compressed_data)
        assert DirStream.from_bytes(decompressed_data) == expected
