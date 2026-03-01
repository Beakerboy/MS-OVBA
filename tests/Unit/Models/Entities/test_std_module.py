from ms_ovba.Models.Entities.std_module import StdModule
from ms_ovba.Models.Entities.module_base import ModuleBase
from unittest.mock import patch, MagicMock


@patch.object(ModuleBase, "__init__")
def test_set_get_cache(mock_base_init) -> None:
    mock_super_init.return_value = None
    module = StdModule("Module1")
    cache = b'foo'
    module.set_cache(cache)
    assert module.get_cache() == cache


#def test_get_name() -> None:
#    module = StdModule("Module1")
#    assert module.get_name() == "Module1"
