import binascii
import re
from ms_ovba_crypto import MsOvbaCrypto
from ms_ovba.vbaProject import VbaProject
from typing import TypeVar


T = TypeVar('T', bound='Project')


class Project:
    """
    The Project data view for the vbaProject
    """
    def __init__(self: T, project: VbaProject) -> None:
        self._project = project
        # Attributes

        # A list of attributes and values
        self.attributes = project.attributes

        # The HostExtenderInfo string
        guid = "{3832D640-CF90-11CF-8E43-00A0C911005A}"
        self.hostExtenderInfo = "&H00000001=" + guid + ";VBE;&H00000000"

    def add_attribute(self: T, name: str, value: str) -> None:
        self.attributes[name] = value

    def __str__(self: T) -> str:
        # Use \x0D0A line endings.
        project = self._project
        project_id = project.project_id
        result = [f'ID="{project_id}"']
        modules = project.modules
        for module in modules:
            result += [module.to_project_module_string()]
        result += ['Name="VBAProject"']
        result += ['HelpContextID="' + str(project.help_context_id) + '"']
        for name, value in self.attributes.items():
            result += [f'{name}="{value}"']
        cmg = MsOvbaCrypto.encrypt(project_id, project.protection_state)
        dpb = MsOvbaCrypto.encrypt(project_id, project.password)
        gc = MsOvbaCrypto.encrypt(project_id, project.visibility_state)
        result += [f'CMG="{binascii.hexlify(cmg).upper().decode("ascii")}"']
        result += [f'DPB="{binascii.hexlify(dpb).upper().decode("ascii")}"']
        result += [f'GC="{binascii.hexlify(gc).upper().decode("ascii")}"']
        result += ['']
        result += ['[Host Extender Info]']
        result += [self.hostExtenderInfo]
        result += ['']
        result += ['[Workspace]']
        for module in modules:
            separator = ", "
            joined = module.modName.value + '='
            joined += separator.join(map(str, module.workspace))
            result += [joined]
        return "\r\n".join(result) + "\r\n"

    def to_bytes(self: T) -> bytes:
        codepage_name = self._project.codepage_name
        return bytes(str(self), codepage_name)

    def write_file(self: T) -> None:
        bin_f = open("project.bin", "wb")
        bin_f.write(self.to_bytes())
        bin_f.close()

    def is_valid(self: T, filename: str) -> bool:
        # get codepage
        # verify that characterset is mbcs with the codepage
    
        with open(filename, 'r') as file:
            for line in file:
                if line[-2:] not in ["\r\n", "\n\r"]:
                    return False
        with open(filename, 'r') as file:
            line = file.readline().strip()
            if not self._valid_project_id_line(line):
                return False
            line = file.readline().strip()
            while self._project_item_line(line[i]):
                if not self._valid_project_item_line(line):
                    return False
                line = file.readline().strip()
            if self._help_file_line(line):
            i += 1
            if not self._valid_help_file_line(lines[i]):
                return False
        if self._exe_line(lines[i]):
            i += 1
            if not self._valid_exe_line(lines[i]):
                return False
        if not self._valid_name_line(lines[i]):
            return False
        i += 1
        if not self._valid_help_id_line(lines[i]):
            return False
        i += 1
        return valid
        
    def _valid_project_id_line(self: T, line: str) -> bool:
        if line[:3] != 'ID="':
            return False
        if line[26:] != '"':
            return False
        guid = line[4:24]
        hd = '[0-9a-fA-F]'
        pattern = (
            r'^\{' + hd + '{8}-' +
            hd + '{4}-' + hd + '{4}-' +
            hd + '{4}-' + hd + r'{12}\}$'
        )
        # Use re.fullmatch to ensure the entire string is evaluated
        return bool(re.fullmatch(pattern, guid))
