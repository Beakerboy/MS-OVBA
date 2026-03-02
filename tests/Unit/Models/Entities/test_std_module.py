from unittest import mock
from ms_ovba.Models.Entities.std_module import StdModule


path = "ms_ovba.Models.Entities.std_module.ModuleBase.__init__"


@patch(path, return_value=None)
def test_construct(mock_base_init) -> None:
    module = StdModule("Module1")
    mock_base_init.assert_called_once_with("Module1")

    assert isinstance(module, StdModule)
    assert module.type == "Module"
    assert not hasattr(module, 'modName')


# def test_get_name() -> None:
#    module = StdModule("Module1")
#    assert module.get_name() == "Module1"
