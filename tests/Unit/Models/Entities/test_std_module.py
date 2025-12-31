from ms_ovba.Models.Entities.std_module import StdModule


def test_set_get_cache() -> None:
    module = StdModule("Module1")
    cache = b'foo'
    module.set_cache(cache)
    assert module.get_cache() == cache


def test_get_name() -> None:
    module = StdModule("Module1")
    assert module.get_name() == "Module1"
