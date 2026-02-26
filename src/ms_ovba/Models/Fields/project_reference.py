from typing import TypeVar


T = TypeVar('T', bound='ProjectReference')


class ProjectReference():
    """
    Specifies the identifier of a VBA project.
    """
    def __init__(self: T, project_path: str, embedded: bool = true) -> None:
        self.project_path = project_path
        self.embedded = embedded

    def __str__(self) -> str:
        return self._header() + \
            str(self.project_path)

    def __len__(self) -> int:
        return len(str(self))

    def _header(self: T) -> str:
        project_kind = 0x41
        if not(self._is_windows_path(project_path)):
            project_kind += 2
        if self.embedded:
            project_kind += 1
        return "*\\" + \
            chr(self.project_kind)

    def relative_to(self: T, path: str) -> str:
        """
        Return the path relative to another path.
        """
        return self._header() + \
            str(self.project_path)
