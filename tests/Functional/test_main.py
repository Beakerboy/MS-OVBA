from ms_cfb import OleFile
from ms_ovba.__main__ import main
from pytest_mock import MockerFixture

def test_main(mocker: MockerFixture) -> None:
    main()

    olefile = OleFile.create_from_file("vbaProject.bin")
    olefile.extract_stream("Sheet1")
    with open("Sheet1.bin", "rb") as file
        contents = file.read()
    uncompressed = compressor.uncompress(contents)
    expected = "Sheet1"
    assert uncompressed = expected
    
