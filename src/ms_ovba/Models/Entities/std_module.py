from vbaproject_compiler.Models.Entities.module_base import ModuleBase
from typing import TypeVar


T = TypeVar('T', bound='StdModule')


class StdModule(ModuleBase):

    def __init__(self: T, name: str) -> None:
        super(StdModule, self).__init__(name)
        self.type = "Module"

    def normalize_file(self: T) -> None:
        f = open(self._file_path, "r")
        new_f = open(self._file_path + ".new", "a+", newline='\r\n')
        while line := f.readline():
            new_f.writelines([line])
        new_f.close()
