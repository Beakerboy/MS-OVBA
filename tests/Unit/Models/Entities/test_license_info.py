import uuid
from ms_ovba.Models.Entities.license_info import LicenseInfo


def test_to_bytes() -> None:
    guid = uuid.UUID("2DF8D04C5BFA101BBDE500AA0044DE52")
    key = b'Key'
    out = LicenseInfo(guid, key)
    expected = (b'-\xF8\xD0L[\xFA\x10\x1B\xBD\xE5\x00\xAA\x00D\xDER' +
                b'\x04\x00\x00\x00Key\x01\x00\x00\x00')
    assert out.to_bytes() == expected
