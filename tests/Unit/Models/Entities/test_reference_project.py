from ms_ovba.Models.Entities.reference_project import ReferenceProject
from ms_ovba.Models.Fields.project_reference import ProjectReference


def test_constructor() -> None:
    ref = ProjectReference("C:/")
    module = ReferenceProject("cp1", ref)

    assert isinstance(module, ReferenceProject)

def test_pack() -> None:
    ref = ProjectReference("")
    
    expected = b'000E00180003673A2F00012E65BE02570017'
    codepage = 0x04E4
    codepage_name = "cp" + str(codepage)
    module = ReferenceProject(codepage_name, ref)
    results = module.pack(codepage_name, 'little')
    assert results == expected
