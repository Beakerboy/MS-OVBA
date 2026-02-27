from ms_ovba.Models.Fields.project_reference import ProjectReference


def test_constructor1() -> None:
    ref = ProjectReference("C:\\Example Path\\Example-ReferencedProject.xls")
    assert isinstance(ref, ProjectReference)


def test_constructor2() -> None:
    path = "C:\\Example Path\\Example-ReferencedProject.xls"
    ref = ProjectReference(path, False)
    assert isinstance(ref, ProjectReference)


def test_len() -> None:
    ref = ProjectReference("C:\\Example Path\\Example-ReferencedProject.xls")
    assert len(ref) == 48


def test_str() -> None:
    ref = ProjectReference("C:\\Example Path\\Example-ReferencedProject.xls")
    assert str(ref) == "*\\CC:\\Example Path\\Example-ReferencedProject.xls"
