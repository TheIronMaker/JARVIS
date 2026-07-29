# jarvis/utils/services/path_resolver/path_resolver.py
from pathlib import Path
from platformdirs import user_config_dir, user_data_dir, user_cache_dir # Eventually Logs and State

from jarvis.core_modules.files.file_loader import FileLoader
from jarvis.core_modules.files.format_drivers import FORMATS

# This is a good framework to build on. Just need to handle the errors different than `raise` errors
# Should also rebuild extension handling with `re` parsing for multiple file formats

"""
Plan (config):
Check if a config file exists in the correct place in platformdirs.user_config_dir
If not, use importlib.resources to read the config file from jarvis and copy it to the user's config directory.
It should load the file from the user's directory from then on.
"""

# To possibly load from internal config file of .py format
SCHEMA_ROOT = {
        "CORE": Path(__file__).resolve().parents[3],
        "PACKAGE": Path(__file__).resolve().parents[6],
        "PROJECT": Path(__file__).resolve().parents[7],
        "CONFIG": Path(user_config_dir("jarvis")),
        "DATA": Path(user_data_dir("jarvis")),
        "CACHE": Path(user_cache_dir("jarvis"))
    }


class PathResolver:
    """
    A utility class for resolving file paths based on a defined schema.
    
    Capabilities:
    - Resolving paths based on a root schema that defines base directories for different domains (e.g., project, config, cache, data).
    - Attaching and separating file extensions.
    - Loading files based on their resolved paths and formats using a format schema that maps file extensions to loader functions.
    - Handling errors for invalid domains, unsupported file formats, and missing files.
    """

    @classmethod
    def _attach_ext(cls, filename: str, extension: str=None) -> str:
        """ Attaches the extension to the filename if it's not already present.
        Args:
            filename (str): The name of the file (with or without extension).
            extension (str, optional): The file extension (e.g., ".json", ".txt).
        Returns:
            str: The filename with the extension attached if it was not already present.
        """
        return filename if not extension or filename.endswith(extension) else filename + cls._format_ext(extension)

    @staticmethod
    def _separate_ext(filename: str|Path) -> tuple[str, str]:
        path = Path(filename)
        return path.stem, path.suffix

    @staticmethod
    def _format_ext(extension: str) -> str:
        """Ensures the extension starts with a dot."""
        return extension if extension.startswith(".") else f".{extension}"

    @classmethod
    def resolve_path(
        cls,
        filename: str,
        extension: str=None,
        domain: str="package",
        location: str|Path=None
        ) -> Path:
        
        """ Resolves a file path based on the given parameters and the defined schema.
        Args:
            filename (str): The name of the file (with or without extension).
            extension (str, optional): The file extension (e.g., ".json", ".txt").
            domain (str, optional): The domain/category of the file e.g., "package" (default), "config", "cache", "data"
            location (str | Path, optional): A specific location to look in before checking the schema.
        Returns:
            path (Path): The resolved file path.
        Raises:
            ValueError: If the domain is not valid.
            FileNotFoundError: If the file is not found in the resolved path.
        """

        # Finds Path class directory based on domain
        path = SCHEMA_ROOT.get(domain.upper())
        if not path:
            print("format not here")
            raise ValueError(f"Invalid domain '{domain}'. Valid domains are: {', '.join(SCHEMA_ROOT.keys())}")
        
        if location:
            path /= location

        path /= cls._attach_ext(filename, extension)
        return path

    @classmethod
    def load_file(
        cls,
        filename: str,
        extension: str=None,
        domain: str="package",
        location: str|Path=None,
        config:dict={}
        ) -> any:

        """ Loads a file based on the resolved path and returns its contents.
        Args:
            filename (str): The name of the file (extension may be provided in the extension field).
            extension (str, optional): The file extension/type.
            domain (str, optional): The domain/category of the file e.g., "package" (default), "config", "cache", "data"
            location (str | Path, optional): A specific location to look in before checking the schema.
        Returns:
            content: The contents of the loaded file.
        Raises:
            ValueError: If the domain is not valid or if the filename does not match the specified type.
            FileNotFoundError: If the file is not found in the resolved path.
        """
        
        path = cls.resolve_path(filename, extension, domain, location)
        ext = cls._format_ext(extension) if extension else path.suffix

        if ext.lower() not in FORMATS:
            raise ValueError(f"Unsupported file format '{ext}'. Currently supported formats: {', '.join(FORMATS)}")

        data = FileLoader.load_file(path, config)
        return data
