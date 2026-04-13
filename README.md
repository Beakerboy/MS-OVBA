[![Python package](https://github.com/Beakerboy/MS-OVBA/actions/workflows/python-package.yml/badge.svg?branch=main)](https://github.com/Beakerboy/MS-OVBA/actions/workflows/python-package.yml)
[![Coverage Status](https://coveralls.io/repos/github/Beakerboy/MS-OVBA/badge.svg?branch=main)](https://coveralls.io/github/Beakerboy/MS-OVBA?branch=main)
# MS-OVBA
Construct and deconstruct the vbaProject.bin that houses VBA code in Microsoft Excel.

## Command Line Interface
```bash
ms_ovba [source directory]
```

## VBAProject Class
The vbaProject class contains all the data and metadata that is used to create the OLE container. It can use this data to create several files, then compress and combine them into an OLE container

```python
from ms_ovba.vbaProject import VbaProject
from ms_cfb.ole_file import OleFile


project = VbaProject()
thisWorkbook = DocModule("ThisWorkbook")
thisWorkbook.addFile(path)
project.addModule(thisWorkbook)

ProjectOleFile.write_file(project)
```

The VbaProject class has many layers of customization available. For example a library reference can be added to the project.

```python
codePage = 0x04E4
codePageName = "cp" + str(codePage)
libidRef = ReferenceRecord(codePageName, LibidReference(
    "{00020430-0000-0000-C000-000000000046}",
    "2.0",
    "0",
    "C:\\Windows\\System32\\stdole2.tlb",
    "OLE Automation"
))
oleReference = Reference(codePageName, libidRef, "stdole")
project.addReference(oleReference)
```
