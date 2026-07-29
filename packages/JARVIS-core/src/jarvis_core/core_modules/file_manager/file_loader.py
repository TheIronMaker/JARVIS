from pathlib import Path
import importlib


class FileLoader:

    def _load_driver(path: Path):
        format = path.suffix[1:].lower()
        loc = f"jarvis_core.core_modules.file_manager.format_drivers.{format}"
        try:
            return importlib.import_module(loc)
        except ModuleNotFoundError:
            raise ValueError(f"Unsupported file format: {format}")


    def load_file(path: Path, config: dict = {}):
        """Load a file based on its format."""
        driver = FileLoader._load_driver(path)
        try:
            return driver.load(path, config)
        except:
            raise FileNotFoundError(f"Unable to load {path.suffix} file located at:", path)
