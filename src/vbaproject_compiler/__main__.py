import argparse
import glob
import os
import uuid
from vbaproject_compiler.vbaProject import VbaProject
from vbaproject_compiler.Models.Entities.doc_module import DocModule
from vbaproject_compiler.Models.Entities.std_module import StdModule
from vbaproject_compiler.Views.project_ole_file import ProjectOleFile
from vbaproject_compiler.Models.Entities.reference_record import (
    ReferenceRecord
)
from vbaproject_compiler.Models.Fields.libid_reference import LibidReference


def main() -> None:

    parser = argparse.ArgumentParser()
    parser.add_argument("directory",
                        help="The directory that contains your files.")
    parser.add_argument("-c", "--create", action="store_true",
                        help="Create an vbaProject.bin from a directory.")
    help_string = ("Display metadata on the project and list the modules that "
                   "it contains.")
    parser.add_argument("-l", "--list", action="store_true",
                        help=help_string)
    parser.add_argument("-x", "--extract", action="store_true",
                        help="Extract files from an OLE file to a directory.")
    args = parser.parse_args()
    if args.create:
        main_create(args)


def main_create(args: argparse.Namespace) -> None:
    # build a list of all bas, cls, frm, and frx files
    bas_files = glob.glob(args.directory + '/**/*.bas', recursive=True)
    # cls_files = glob.glob('*.cls')
    # frm_files = glob.glob('*.frm')
    # frx_files = glob.glob('*.frx')

    # create a new project object
    project = VbaProject()

    # add default modules
    module = DocModule('Sheet1')
    base_path = os.path.dirname(__file__)
    module.add_file(base_path + '/blank_files/Sheet1.cls')
    module.normalize_file()
    guid = uuid.UUID("0002082000000000C000000000000046")
    module.set_guid(guid)
    project.add_module(module)
    module = DocModule('ThisWorkbook')
    module.add_file(base_path + '/blank_files/ThisWorkbook.cls')
    module.normalize_file()
    guid = uuid.UUID("0002081900000000C000000000000046")
    module.set_guid(guid)
    project.add_module(module)
    project.set_project_id('{9E394C0B-697E-4AEE-9FA6-446F51FB30DC}')
    # add the files
    for file_path in bas_files:
        file_name = os.path.basename(file_path)
        file = os.path.splitext(file_name)
        code = StdModule(file[0])
        code.add_file(file_path)
        code.normalize_file()
        project.add_module(code)
    codepage = 0x04E4
    codepage_name = "cp" + str(codepage)
    libid_ref = LibidReference(
        uuid.UUID("0002043000000000C000000000000046"),
        "2.0",
        "0",
        "C:\\Windows\\System32\\stdole2.tlb",
        "OLE Automation"
    )
    ole_reference = ReferenceRecord(codepage_name, "stdole", libid_ref)
    libid_ref2 = LibidReference(
        uuid.UUID("2DF8D04C5BFA101BBDE500AA0044DE52"),
        "2.0",
        "0",
        "C:\\Program Files\\Common Files\\Microsoft Shared\\OFFICE16\\MSO.DLL",
        "Microsoft Office 16.0 Object Library"
    )
    office_reference = ReferenceRecord(codepage_name, "Office", libid_ref2)
    project.add_reference(ole_reference)
    project.add_reference(office_reference)
    ole_file = ProjectOleFile(project)
    ole_file.write_file()
    file = glob.glob('vbaProject.bin')


if __name__ == '__main__':
    main()
