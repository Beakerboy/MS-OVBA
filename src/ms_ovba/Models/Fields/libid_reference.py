import uuid
from typing import TypeVar


T = TypeVar('T', bound='LibidReference')


class LibidReference():
    """
    2.1.1.8

    LibidReference = "*\" LibidReferenceKind LibidGuid
    "#" LibidMajorVersion "." LibidMinorVersion
    "#" LibidLcid
    "#" LibidPath
    "#" LibidRegName
    LibidReferenceKind = %x47 / %x48
    LibidGuid = GUID
    LibidMajorVersion = 1*4HEXDIG
    LibidMinorVersion = 1*4HEXDIG
    LibidLcid = 1*8HEXDIG
    LibidPath = *(%x01-22 / %x24-FF)
    LibidRegName = *255(%x01-FF)
    """
    def __init__(self: T, libid_guid: uuid.UUID, version: str,
                 libid_lcid: str, libid_path: str,
                 libid_reg_name: str) -> None:
        self._libid_guid = libid_guid
        self._version = version
        self._libid_lcid = libid_lcid
        self._libid_path = libid_path
        self._libid_reg_name = libid_reg_name
        if self._is_windows_path(libid_path):
            self._libid_reference_kind = "G"
        else:
            self._libid_reference_kind = "H"

    def __str__(self: T) -> str:
        return "*\\" + \
            self._libid_reference_kind + \
            "{" + str(self._libid_guid).upper() + "}#" + \
            self._version + "#" + \
            self._libid_lcid + "#" + \
            str(self._libid_path) + "#" + \
            self._libid_reg_name

    def __len__(self: T) -> int:
        return len(str(self))

    def _is_windows_path(self: T, path: str) -> bool:
        return path[0] != '/'
