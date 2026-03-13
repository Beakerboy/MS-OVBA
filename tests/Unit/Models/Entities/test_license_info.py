import uuid
from ms_ovba.Models.Entities.license_info import LicenseInfo


def test_to_bytes() -> None:
  uuid = uuid.UUID("2DF8D04C5BFA101BBDE500AA0044DE52")
  key = b'Key'
  out = LicenseInfo(uuid, key)
  expected = (b'\x2D\xF8\xD0\x4C\x5B\xFA\x10\x1B\xBD\xE5\x00\xAA\x00\x44\xDE\x52' +
              b'\x04\x00\x00\x00Key\x04\x00\x00\x00')
  assert out.to_bytes() == expected
