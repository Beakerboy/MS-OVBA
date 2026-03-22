from ms_ovba_compression.ms_ovba import MsOvba
from ms_ovba.Models.Fields.doubleEncodedString import (
    DoubleEncodedString
)
from ms_ovba.Models.Fields.packed_data import PackedData
from ms_ovba.Models.Fields.idSizeField import IdSizeField
from typing import TypeVar


T = TypeVar('T', bound='ModuleBase')


class ModuleBase():
    def __init__(self: T, name: str) -> None:
        """
        Initialize the module record
        """
        self.modName = DoubleEncodedString([0x0019, 0x0047], name)
        self.streamName = DoubleEncodedString([0x001A, 0x0032], name)
        self.docString = DoubleEncodedString([0x001C, 0x0048], "")
        self.helpContext = IdSizeField(0x001E, 4, 0)
        self._cookie = IdSizeField(0x002C, 2, 0xFFFF)

        # self.readonly = SimpleRecord(0x001E, 4, helpContext)
        # self.private = SimpleRecord(0x001E, 4, helpContext)
        self._cache = b''
        self.workspace = [0, 0, 0, 0, 'C']
        self.type = ''
        self.created = 0
        self.modified = 0
        self._fileSize = 0
        self._size = 0

        # GUIDs
        self._guids: str[] = []

    @property
    def guids(self: T) -> str[]:
        return self._guids

    @guids.setter
    def guids(self: T, guid: str) -> None:
        if isinstance(guid, list):
            self._guids = guid
        else:
            self._guids = [guid]

    def add_guid(self: T, guid: str) -> None:
        """
        Append a guid to the list
        """
        self._guids += [guid]

    @property
    def cache(self: T) -> bytes:
        return self._cache

    @cache.setter
    def cache(self: T, cache: bytes) -> None:
        self._cache = cache

    @property
    def cookie(self: T) -> int:
        return self._cookie.value

    @cookie.setter
    def cookie(self: T, value: int) -> None:
        self._cookie = IdSizeField(0x002C, 2, value)

    @property
    def name(self: T) -> str:
        return self.modName.value

    @property
    def bin_path(self: T) -> str:
        return self._file_path + ".bin"

    def add_workspace(self: T, val1: int, val2: int,
                      val3: int, val4: int, val5: int) -> None:
        self.workspace = [val1, val2, val3, val4, val5]

    def pack(self: T, endien: str, cp_name: str) -> bytes:
        """
        Pack the metadata for use in the dir stream.
        """
        typeid_value = 0x0022 if self.type == 'Document' else 0x0021
        type_id = PackedData("HI", typeid_value, 0)
        self.offsetRec = IdSizeField(0x0031, 4, len(self._cache))
        output = (self.modName.pack(endien, cp_name)
                  + self.streamName.pack(endien, cp_name)
                  + self.docString.pack(endien, cp_name)
                  + self.offsetRec.pack(endien)
                  + self.helpContext.pack(endien, cp_name)
                  + self._cookie.pack(endien)
                  + type_id.pack(endien))
        footer = PackedData("HI", 0x002B, 0)
        output += footer.pack(endien)
        return output

    def to_project_module_string(self: T) -> str:
        return self.type + "=" + self.modName.value

    def add_file(self: T, file_path: str) -> None:
        self._file_path = file_path

    def write_file(self: T) -> None:
        bin_f = open(self._file_path + ".bin", "wb")
        bin_f.write(self._cache)
        with open(self._file_path + ".new", mode="rb") as new_f:
            contents = new_f.read()
        ms_ovba = MsOvba()
        compressed = ms_ovba.compress(contents)
        bin_f.write(compressed)
        bin_f.close()

    def _attr(self: T, name: str, value: str) -> str:
        return 'Attribute VB_' + name + ' = ' + value + '\n'
