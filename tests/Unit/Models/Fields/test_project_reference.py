from ms_ovba.Models.Fields.project_reference import ProjectReference


def test_constructor() -> None:
    ref = ProjectReference("C:\\Example Path\\Example-ReferencedProject.xls")
    assert isinstance(ref, ReferenceProject)


def test_constructor() -> None:
    ref = ProjectReference("C:\\", False)
    assert isinstance(module, ReferenceProject)


def test_len() -> None:
    ref = ProjectReference("C:\\Example Path\\Example-ReferencedProject.xls")
    assert len(ref) == 48


def test_str() -> None:
    ref = ProjectReference("C:\\Example Path\\Example-ReferencedProject.xls")
    assert str(ref) == "*\\CC:\\Example Path\\Example-ReferencedProject.xls"
