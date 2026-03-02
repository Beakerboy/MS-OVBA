from unittest import mock
from ms_ovba.Models.Entities.std_module import StdModule


class MockBase:
    called = False

    def __init__(self, foo) -> None:
        self.called = True


def test_construct() -> None:
    path = "ms_ovba.Models.Entities.std_module.ModuleBase"
    with mock.patch(path, MockBase):
        module = StdModule("Module1")

        assert isinstance(module, StdModule)
        assert module.type == "Module"
        assert not hasattr(module, 'modName')
        assert MockBase.called


# def test_get_name() -> None:
#    module = StdModule("Module1")
#    assert module.get_name() == "Module1"
