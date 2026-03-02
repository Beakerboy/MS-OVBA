from unittest import mock
from ms_ovba.Models.Entities.std_module import StdModule


path = "ms_ovba.Models.Entities.std_module.ModuleBase"


@mock.patch(path)
def test_construct(mock_path) -> None:
    module = StdModule("Module1")
    # assert mock_path.called
    assert isinstance(module, StdModule)
    assert module.type == "Module"
    assert not hasattr(module, 'modName')


# def test_get_name() -> None:
#    module = StdModule("Module1")
#    assert module.get_name() == "Module1"
