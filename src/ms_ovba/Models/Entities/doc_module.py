from ms_ovba_compression.ms_ovba import MsOvba
from vbaproject_compiler.Models.Entities.module_base import ModuleBase
from typing import TypeVar


T = TypeVar('T', bound='DocModule')


class DocModule(ModuleBase):
    """
    A Document Module is a module record that is associated with a worksheet or
    workbook.
    """
    def __init__(self: T, name: str) -> None:
        self.doc_tlib_ver = 0
        super(DocModule, self).__init__(name)
        self.type = "Document"

        # GUIDs
        self._guid = []

    def to_project_module_string(self: T) -> str:
        return ("Document=" + self.modName.value + "/&H"
                + self.doc_tlib_ver.to_bytes(4, "big").hex())

    def normalize_file(self: T) -> None:
        f = open(self._file_path, "r")
        new_f = open(self._file_path + ".new", "a+", newline='\r\n')
        for i in range(5):
            line = f.readline()

        new_f.write(line)
        guid_string = '"0'
        for guid in self._guid:
            guid_string += '{' + str(guid).upper() + '}"'
        txt = self._attr("Base", guid_string)
        new_f.writelines([txt])
        while line := f.readline():
            new_f.writelines([line])
        new_f.writelines([self._attr("TemplateDerived", "False")])
        new_f.writelines([self._attr("Customizable", "True")])
        new_f.close()

    def write_file(self: T) -> None:
        bin_f = open(self._file_path + ".bin", "wb")
        bin_f.write(self._cache)
        with open(self._file_path + ".new", mode="rb") as new_f:
            contents = new_f.read()
        ms_ovba = MsOvba()
        compressed = ms_ovba.compress(contents)
        bin_f.write(compressed)
        bin_f.close()
