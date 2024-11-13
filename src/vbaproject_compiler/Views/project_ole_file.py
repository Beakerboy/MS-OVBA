from ms_cfb.ole_file import OleFile
from ms_cfb.Models.Directories.root_directory import RootDirectory
from ms_cfb.Models.Directories.storage_directory import StorageDirectory
from ms_cfb.Models.Directories.stream_directory import StreamDirectory
from vbaproject_compiler.vbaProject import VbaProject
from vbaproject_compiler.Views.dirStream import DirStream
from vbaproject_compiler.Views.project_view import ProjectView
from vbaproject_compiler.Views.project import Project
from vbaproject_compiler.Views.projectWm import ProjectWm
from typing import TypeVar


T = TypeVar('T', bound='ProjectOleFile')


class ProjectOleFile:

    def __init__(self: T, project: VbaProject) -> None:
        self._project = project

    def _build_ole_directory(self: T) -> RootDirectory:
        """
        Create all the custom views for the OLE file:
            dir
            project
            projectWm
            vbs_project

        Organize the modules and views into the correct storage directories
        """
        directory = RootDirectory()
        storage = StorageDirectory("VBA")
        for module in self._project.get_modules():
            module.write_file()
            dir = StreamDirectory(module.get_name(), module.get_bin_path())
            storage.add_directory(dir)

        module = DirStream(self._project)
        module.write_file()
        dir = StreamDirectory("dir", "dir.bin")
        storage.add_directory(dir)

        module = ProjectView(self._project)
        module.write_file()
        dir = StreamDirectory("_VBA_PROJECT", "vba_project.bin")
        storage.add_directory(dir)

        directory.add_directory(storage)

        if self._project.get_include_projectwm():
            module = ProjectWm(self._project)
            module.write_file()
            stream = StreamDirectory("PROJECTwm", "projectwm.bin")
            directory.add_directory(stream)

        module = Project(self._project)
        module.write_file()
        stream = StreamDirectory("PROJECT", "project.bin")
        directory.add_directory(stream)
        return directory

    def _write_ole_file(self: T, root: RootDirectory) -> None:
        ole_file = OleFile()
        ole_file.root_directory = root
        ole_file.create_file("vbaProject.bin")

    def write_file(self: T) -> None:
        directory = self._build_ole_directory()
        self._write_ole_file(directory)
