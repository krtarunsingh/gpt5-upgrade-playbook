import importlib.util, sys, pathlib

def load_module(path):
    spec = importlib.util.spec_from_file_location("mod", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore
    return mod

def test_normalize_name():
    mod = load_module(str(pathlib.Path("examples/foo.py").resolve()))
    f = mod.normalize_name
    assert f(" alice ") == "Alice"
    assert f("bob  ") == "Bob"
    assert f("  ") == ""
