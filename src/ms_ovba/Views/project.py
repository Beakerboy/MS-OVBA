import binascii
from ms_ovba_crypto.ms_ovba_crypto import MsOvbaCrypto
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
        result = [f'ID="{project_id}"']
        modules = project.modules
        for module in modules:
            result += [module.to_project_module_string()]
        result += ['Name="VBAProject"']
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
        codepage_name = self.project.codepage_name
        return bytes(str(self), codepage_name)

    def write_file(self: T) -> None:
        bin_f = open("project.bin", "wb")
        bin_f.write(self.to_bytes())
        bin_f.close()
