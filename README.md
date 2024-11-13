[![Coverage Status](https://coveralls.io/repos/github/Beakerboy/vbaProject-Compiler/badge.svg?branch=main)](https://coveralls.io/github/Beakerboy/vbaProject-Compiler?branch=main)
# vbaProject-Compiler
Create a vbaProject.bin file from VBA source files.


## Command Line Interface
Eventually it will ne possible to use the CLI to creatr a vbaProject.bin file from source files and an optional configuration file.

## VBAProject Class
The vbaProject class contains all the data and metadata that is used to create the OLE container.

```python
from vbaProjectCompiler.vbaProject import VbaProject
from ms_cfb.ole_file import OleFile


project = VbaProject()
thisWorkbook = DocModule("ThisWorkbook")
thisWorkbook.addFile(path)
project.addModule(thisWorkbook)

ole_file = OleFile(project)
ole_file.create_file(".")
```

The VbaProject class has many layers of customization available. For example a library referenece can be added to the project.

```python
codePage = 0x04E4
codePageName = "cp" + str(codePage)
libidRef = LibidReference(
    "{00020430-0000-0000-C000-000000000046}",
    "2.0",
    "0",
    "C:\\Windows\\System32\\stdole2.tlb",
    "OLE Automation"
)
oleReference = ReferenceRecord(codePageName, "stdole", libidRef)
project.addReference(oleReference)
```
