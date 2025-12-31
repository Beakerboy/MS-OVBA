import pytest
from ms_ovba.Models.Fields.idSizeField import IdSizeField


def test_bad_value() -> None:
    field = IdSizeField(2, 3, 6)
    with pytest.raises(Exception):
        field.pack(1234, "little")
