from unittest import mock
from ms_ovba.Models.Entities.std_module import StdModule


class MockBase:
    called = False

    def __init__(self, foo) -> None:
        self.called = True


def test_construct() -> None:
    path = "ms_ovba.Models.Entities.std_module.ModuleBase"
    with mock.patch.object(path, "__init__") as mock_super_init:
        mock_super_init.return_value = None
        module = StdModule("Module1")
        mock_super_init.assert_called_once_with("Module1")

        assert isinstance(module, StdModule)
        assert module.type == "Module"
        assert not hasattr(module, 'modName')


# def test_get_name() -> None:
#    module = StdModule("Module1")
#    assert module.get_name() == "Module1"
