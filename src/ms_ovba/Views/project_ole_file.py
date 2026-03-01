from ms_cfb.ole_file import OleFile
from ms_cfb.Models.Directories.root_directory import RootDirectory
from ms_cfb.Models.Directories.storage_directory import StorageDirectory
from ms_cfb.Models.Directories.stream_directory import StreamDirectory
from ms_ovba.vbaProject import VbaProject
from ms_ovba.Views.dirStream import DirStream
from ms_ovba.Views.project_view import ProjectView
from ms_ovba.Views.project import Project
from ms_ovba.Views.projectWm import ProjectWm
from typing import TypeVar


T = TypeVar('T', bound='ProjectOleFile')


class ProjectOleFile:

    @staticmethod
    def _build_ole_directory(project: VBAProject) -> RootDirectory:
        """
        Create all the custom views for the OLE file:
            dir
            project
            projectWm
            vbs_project

        Organize the modules and views into the correct storage directories
        """
        directory = RootDirectory()
        directory.set_modified(project.default_date)
        storage = StorageDirectory("VBA")
        storage.set_created(project.default_date)
        storage.set_modified(project.default_date)
        for module in project.get_modules():
            module.write_file()
            dir = StreamDirectory(module.get_name(), module.get_bin_path())
            storage.add_directory(dir)

        module = DirStream(project)
        module.write_file()
        dir = StreamDirectory("dir", "dir.bin")
        storage.add_directory(dir)

        module = ProjectView(project)
        module.write_file()
        dir = StreamDirectory("_VBA_PROJECT", "vba_project.bin")
        storage.add_directory(dir)

        directory.add_directory(storage)

        if self._project.get_include_projectwm():
            module = ProjectWm(project)
            module.write_file()
            stream = StreamDirectory("PROJECTwm", "projectwm.bin")
            directory.add_directory(stream)

        module = Project(project)
        module.write_file()
        stream = StreamDirectory("PROJECT", "project.bin")
        directory.add_directory(stream)
        return directory

    @staticmethod
    def _write_ole_file(root: RootDirectory) -> None:
        ole_file = OleFile()
        ole_file.root_directory = root
        ole_file.create_file("vbaProject.bin")

    @staticmethod
    def write_file(project: VBAProject) -> None:
        directory = ProjectOleFile._build_ole_directory(project)
        ProjectOleFile._write_ole_file(directory)
