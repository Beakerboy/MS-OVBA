import binascii
import ms_ovba_crypto
from ms_ovba.vbaProject import VbaProject
from typing import TypeVar


T = TypeVar('T', bound='Project')


class Project:
    """
    The Project data view for the vbaProject
    """
    def __init__(self: T, project: VbaProject) -> None:
        self.project = project
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
        project = self.project
        project_id = project.project_id
        eol = "\r\n"
        result = f'ID="{project_id}"' + eol
        modules = project.modules
        for module in modules:
            result += module.to_project_module_string() + eol
        result += 'Name="VBAProject"' + eol
        for key in self.attributes:
            result += f'{name}="{value}"' + eol
        cmg = ms_ovba_crypto.encrypt(
            project_id, project.protection_state
        )
        dpb = ms_ovba_crypto.encrypt(project_id, project.password)
        gc = ms_ovba_crypto.encrypt(project_id, project.visibility_state)
        result += 'CMG="' + binascii.hexlify(cmg).upper().decode('ascii') + '"' + eol
        result += 'DPB="' + binascii.hexlify(dpb).upper().decode('ascii') + '"' + eol
        result += 'GC="' + binascii.hexlify(gc).upper().decode('ascii') + '"' + eol
        result += eol
        result += '[Host Extender Info]' + eol
        result += self.hostExtenderInfo
        result += eol * 2
        result += '[Workspace]' + eol
        for module in modules:
            separator = ", "
            result += module.modName.value + '='
            joined = separator.join(map(str, module.workspace))
            result += joined + eol
        return result

    def to_bytes(self: T) -> bytes:
        codepage_name = self.project.codepage_name
        return bytes(str(self), codepage_name)

    def write_file(self: T) -> None:
        bin_f = open("project.bin", "wb")
        bin_f.write(self.to_bytes())
        bin_f.close()
