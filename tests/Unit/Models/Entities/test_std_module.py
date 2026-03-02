from unittest import mock
from ms_ovba.Models.Entities.std_module import StdModule


def test_construct() -> None:
    cache = b'foo'
    path = "ms_ovba.Models.Entities.std_module.ModuleBase"
    with mock.patch(path) as MockSuper:
        module = StdModule("Module1")
        assert isinstance(module, StdModule)
        assert module.type == "Module"
        assert module.modname == None


#def test_get_name() -> None:
#    module = StdModule("Module1")
#    assert module.get_name() == "Module1"
