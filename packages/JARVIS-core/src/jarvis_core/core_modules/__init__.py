import pkgutil
import importlib
import logging

_log = logging.getLogger(__name__)
_available = {name for _, name, _ in pkgutil.iter_modules(__path__)}
_failed: dict[str, Exception] = {}

__all__ = list(_available)

def __getattr__(name: str):
    if name in globals():
        return globals()[name]

    if name not in _available:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    if name in _failed:
        raise ImportError(
            f"{__name__}.{name} previously failed to import"
        ) from _failed[name]

    try:
        module = importlib.import_module(f"{__name__}.{name}")
    except Exception as e:
        _failed[name] = e
        _log.error("Failed to load core module %r: %s", name, e)
        raise

    globals()[name] = module
    return module

def __dir__():
    return sorted(_available)
