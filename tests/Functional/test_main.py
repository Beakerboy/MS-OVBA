from ms_cfb.ole_file import OleFile
from ms_ovba.__main__ import main
from ms_ovba_compression.ms_ovba import MsOvba
from pytest_mock import MockerFixture


def test_main(mocker: MockerFixture) -> None:
    mocker.patch(
        "sys.argv",
        [
            "ms_ovba.py",
            ".",
        ],
    )
    main()

    olefile = OleFile.create_from_file("vbaProject.bin")
    olefile.extract_stream("Sheet1", ".")
    with open("Sheet1.bin", "rb") as file:
        contents = file.read()
    compressor = MsOvba()
    uncompressed = compressor.decompress(contents)
    expected = "Sheet1"
    assert uncompressed == expected
    
