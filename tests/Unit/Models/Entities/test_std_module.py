from unittest import mock
from ms_ovba.Models.Entities.std_module import StdModule


def test_construct() -> None:
    path = "ms_ovba.Models.Entities.std_module.ModuleBase"
    with mock.patch(path):
        module = StdModule("Module1")
        assert isinstance(module, StdModule)
        assert module.type == "Module"
        assert module.modName is None


# def test_get_name() -> None:
#    module = StdModule("Module1")
#    assert module.get_name() == "Module1"
