from ms_ovba.Models.Entities.reference_project import ReferenceProject
from ms_ovba.Models.Fields.project_reference import ProjectReference


def test_constructor() -> None:
    ref = ProjectReference("")
    module = ReferenceProject("cp1", ref)

    assert isinstance(module, ReferenceProject)
