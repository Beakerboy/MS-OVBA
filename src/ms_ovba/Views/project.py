import binascii
import re
from ms_ovba_crypto import MsOvbaCrypto
from ms_ovba.vbaProject import VbaProject
from typing import Any, TypeVar


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
        workspace_started = False

        for module in modules:
            if module.workspace is not None:
                if not workspace_started:
                    workspace_started = True
                    result += ['']
                    result += ['[Workspace]']
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

    @staticmethod
    def is_valid(filename: str) -> Any:
        """
        Validate the structure of the file. This method does
        not test if data values match between streams.
        """

        with open(filename, 'r', newline='') as file:
            for line in file:
                if line[-2:] not in ["\r\n", "\n\r"]:
                    return False
        with open(filename, 'r') as file:
            line = file.readline().strip()
            if not Project._valid_project_id_line(line):
                return False
            line = file.readline().strip()
            while Project._project_item_line(line):
                if not Project._valid_project_item_line(line):
                    return False
                line = file.readline().strip()
            if Project._help_file_line(line):
                if not Project._valid_help_file_line(line):
                    return False
                line = file.readline().strip()
            if Project._exe_line(line):
                if not Project._valid_exe_line(line):
                    return False
                line = file.readline().strip()
            if not Project._valid_name_line(line):
                return False
            line = file.readline().strip()
            if not Project._valid_help_id_line(line):
                return False
            line = file.readline().strip()
            if Project._description_line(line):
                if not Project._valid_description_line(line):
                    return False
                line = file.readline().strip()
            if Project._version_line(line):
                if not Project._valid_version_line(line):
                    return False
                line = file.readline().strip()
            if not Project._valid_protection_line(line):
                return False
            line = file.readline().strip()
            if not Project._valid_password_line(line):
                return False
            line = file.readline().strip()
            # if not Project._valid_visibility_line(line):
            #     return False
            # line = file.readline().strip()
            # if line != "":
            #     return False

        return True

    @staticmethod
    def _valid_project_id_line(line: str) -> Any:
        pieces = line.split('=')
        if pieces[0] != 'ID':
            return False
        value = pieces[1]
        if value[0] != '"' or value[-1] != '"':
            return False
        return Project._valid_guid(value[1:-1])

    @staticmethod
    def _project_item_line(line: str) -> bool:
        options = ['Doc', 'Mod', 'Cla', 'Bas', 'Pac']
        return line[:3] in options

    @staticmethod
    def _help_file_line(line: str) -> bool:
        return line[0:5] == 'HelpF'

    @staticmethod
    def _exe_line(line: str) -> bool:
        return line[0:3] == 'Exe'

    @staticmethod
    def _description_line(line: str) -> bool:
        return line[0:3] == 'Des'

    @staticmethod
    def _version_line(line: str) -> bool:
        return line[0:3] == 'Ver'

    @staticmethod
    def _valid_project_item_line(line: str) -> bool:
        # Split at the equals.
        pieces = line.split('=')
        # Verify the name.
        if pieces[0] == 'Document':
            doc_string = pieces[1].split('/')
            return (
                Project._valid_modulename(doc_string[0]) and
                Project._valid_hex32(doc_string[1])
            )
        elif pieces[0] == 'Package':
            pass
        elif pieces[0] in ['Module', 'Class', 'BaseClass']:
            # ToDo: append name to an array for validation
            # against dir-stream
            return Project._valid_modulename(pieces[1])
        return False

    @staticmethod
    def _valid_help_file_line(line: str) -> bool:
        pieces = line.split('=')
        if pieces[0] == "HelpFile":
            return Project._valid_path(pieces[1])
        return False

    @staticmethod
    def _valid_exe_line(line: str) -> bool:
        pieces = line.split('=')
        if pieces[0] == "ExeName32":
            return Project._valid_path(pieces[1])
        return False

    @staticmethod
    def _valid_name_line(line: str) -> bool:
        pieces = line.split('=')
        if pieces[0] == "Name":
            return Project._valid_quoted_string(pieces[1], 1, 128)
        return False

    @staticmethod
    def _valid_help_id_line(line: str) -> bool:
        pieces = line.split('=')
        if pieces[0] == "HelpContextID":
            string = pieces[1]
            if string[0] != '"' or string[-1] != '"':
                return False
            candidate = string[1:-1]
            try:
                int(candidate)
                return True
            except ValueError:
                return False
        return False

    @staticmethod
    def _valid_description_line(line: str) -> bool:
        pieces = line.split('=')
        if pieces[0] == "Description":
            return Project._valid_quoted_string(pieces[1], 0, 2000)
        return False

    @staticmethod
    def _valid_version_line(line: str) -> bool:
        pieces = line.split('=')
        if pieces[0] == "VersionCompatible32":
            return pieces[1] == '"393222000"'
        return False

    @staticmethod
    def _valid_protection_line(line: str) -> bool:
        pieces = line.split('=')
        if pieces[0] == "CMG":
            return Project._valid_quoted_hex(pieces[1], 22, 28)
        return False

    @staticmethod
    def _valid_password_line(line: str) -> bool:
        pieces = line.split('=')
        if pieces[0] == "DPB":
            return Project._valid_quoted_hex(pieces[1], 16, 16)
        return False
        
    # Data Type Validators
    @staticmethod
    def _valid_hex32(hex: str) -> bool:
        prefix = hex[:2]
        value = int(hex[2:], 16)
        min = -2147483648
        max = 2147483647
        return prefix == "&H" and (min <= value <= max)

    @staticmethod
    def _valid_modulename(name: str) -> bool:
        return len(name) <= 31

    @staticmethod
    def _valid_guid(guid: str) -> bool:
        hd = '[0-9a-fA-F]'
        pattern = (
            r'^\{' + hd + '{8}-' +
            hd + '{4}-' + hd + '{4}-' +
            hd + '{4}-' + hd + r'{12}\}$'
        )
        # Use re.fullmatch to ensure the entire string is evaluated
        return bool(re.fullmatch(pattern, guid))

    @staticmethod
    def _valid_path(path: str) -> bool:
        return Project._valid_quoted_string(path, 0, 259)

    @staticmethod
    def _valid_quoted_string(string: str, min: int, max: int) -> bool:
        if not (min + 2 <= len(string) <= max + 2):
            return False
        if string[0] != '"' or string[-1] != '"':
            return False
        string = string[1:-1]
        # Dquot must be paired
        string.replace('""', " ")
        string.replace('\t', " ")
        string.replace('"', '\x19')
        return all(32 <= ord(char) <= 255 for char in string)

    @staticmethod
    def _valid_quoted_hex(string: str, min: int, max: int) -> bool:
        if not (min + 2 <= len(string) <= max + 2):
            return False
        if string[0] != '"' or string[-1] != '"':
            return False
        string = string[1:-1]
        return all(
            ((48 <= ord(char) <= 57) or (65 <= ord(char) <= 70))
            for char in string
        )
