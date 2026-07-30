from pathlib import Path
import importlib


class FileLoader:
    @classmethod
    def _load_driver(cls, path: Path):
        driver_loc = cls.__module__.rsplit('.', 1)[0]
        format = path.suffix[1:].lower()
        loc = f"{driver_loc}.format_drivers.{format}"
        try:
            return importlib.import_module(loc)
        except ModuleNotFoundError:
            raise ValueError(f"Unsupported file format: {format}")

    @staticmethod
    def load_file(path: Path, config: dict = None):
        """Load a file based on its format."""
        driver = FileLoader._load_driver(path)
        try:
            return driver.load(path, config or {})
        except Exception:
            raise FileNotFoundError(f"Unable to load {path.suffix} file located at: {path}")
