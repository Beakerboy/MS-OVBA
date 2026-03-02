import pytest
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


@pytest.mark.parametrize("data, embedded, expected", [
    (
        "C:\\Example Path\\Example-ReferencedProject.xls",
        True,
        "*\\CC:\\Example Path\\Example-ReferencedProject.xls"
    ),
    (
        "/Example Path/Example-ReferencedProject.xls",
        False,
        "*\\B/Example Path/Example-ReferencedProject.xls"
    )
])
def test_str(data, embedded, expected) -> None:
    ref = ProjectReference(data, embedded)
    assert str(ref) == expected


def test_relative() -> None:
    ref = ProjectReference("C:\\Example Path\\Example-ReferencedProject.xls")
    rel = ref.relative()
    assert str(rel) == "*\\CExample-ReferencedProject.xls"
