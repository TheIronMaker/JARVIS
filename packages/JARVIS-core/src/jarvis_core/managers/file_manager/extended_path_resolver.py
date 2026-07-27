
from jarvis_core.managers.file_manager import PathResolver


class ExtendedPathResolver(PathResolver):
    """An extension pack that injects new formats without modifying core files."""
    SCHEMA_FORMAT = {
        **PathResolver.SCHEMA_FORMAT # Add more here
    }