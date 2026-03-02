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


@pytest.mark.parametrize("data, expected", [
    [
        "C:\\Example Path\\Example-ReferencedProject.xls",
        "*\\CC:\\Example Path\\Example-ReferencedProject.xls"
    ],
    [
        "/Example Path/Example-ReferencedProject.xls",
        "*\\B/Example Path/Example-ReferencedProject.xls"
    ]
])
def test_str(data, expected) -> None:
    ref = ProjectReference(data)
    assert str(ref) == expected


def test_relative() -> None:
    ref = ProjectReference("C:\\Example Path\\Example-ReferencedProject.xls")
    rel = ref.relative()
    assert str(rel) == "*\\CExample-ReferencedProject.xls"
