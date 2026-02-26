from typing import TypeVar


T = TypeVar('T', bound='ProjectReference')


class ProjectReference():
    def __init__(self: T, project_path: str, embedded: bool = true) -> None:
        self.project_path = project_path
        self.embedded = embedded

    def __str__(self):
        project_kind = 0x41
        if not(self._is_windows_path(project_path)):
            project_kind += 2
        if self.embedded:
            project_kind += 1
        return "*\\" + \
            chr(self.project_kind) + \
            str(self.project_path)

    def __len__(self):
        return len(str(self))
