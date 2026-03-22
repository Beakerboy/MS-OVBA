from __future__ import annotations
from typing import TypeVar


T = TypeVar('T', bound='ProjectReference')


class ProjectReference():
    """
    2.1.1.12
    Specifies the identifier of a VBA project.

    ProjectReference = "*\" ProjectKind ProjectPath
    ProjectKind = %x41-44
    ProjectPath = *(%x01-FF}
    """
    def __init__(self: T, project_path: str, embedded: bool = True) -> None:
        self._project_path = project_path
        self._embedded = embedded

    # Dunder Methods
    def __str__(self: T) -> str:
        return self._header() + \
            str(self._project_path)

    def __len__(self: T) -> int:
        return len(str(self))

    def relative(self: T) -> ProjectReference:
        """
        Strip off the path and just return the file.
        """
        # Find last '\'
        pos = self._project_path.rfind('\\')

        rel_path = self._project_path[pos + 1:]
        return ProjectReference(rel_path, self._embedded)

    def _header(self: T) -> str:
        project_kind = 0x41
        if not self._is_windows_path(self._project_path):
            project_kind += 1
        if self._embedded:
            project_kind += 2
        return "*\\" + \
            chr(project_kind)

    def _is_windows_path(self: T, path: str) -> bool:
        return path[0] != '/'
