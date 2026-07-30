from pathlib import Path
import inspect

from jarvis.core_modules.files import PathResolver

# Node.describe_topology() could show the node's communication topology for debugging connections
# Must include closing code for channels / __del__ to close sockets and proxy threads - possible data leaking / persistence
class Node:
    def __init__(self, id:str=None, path:str|Path=None):
        if not id:
            # More is needed for creating a new ID. Maybe a signal to make a config file.
            from jarvis.core_modules.security.UUID import generate_UUID
            id = generate_UUID.v7()
        
        self.id = id
        self.path = path
        self.config_paths = []
        self.configs = {}

        # Communication
        self.subs = {}
        self.pubs = {}
        self.proxies = {}

    @property
    def module_dir(self) -> Path:
        """Directory containing the file where *this subclass* is defined."""
        print(inspect.getfile(type(self)))
        return Path(inspect.getfile(type(self))).resolve().parent

    def load_manifest(self, path: str, domain: str="config"):
        self.manifest = PathResolver.load_file(path, domain=domain)
        for path in self.manifest.get("configs", []):
            self.config_paths.append(path)

    def load_configs(self, paths:list):
        self.configs = {path: PathResolver.load_file(path) for path in self.config_paths}

    def create_coms(self): # Must be able to call twice without orphaning previous connections
        print(self.configs)
        zeromq = self.configs.get("zeromq")
        if not zeromq: return

        subs, pubs, proxies = zeromq.get("subs"), zeromq.get("pubs"), zeromq.get("proxies")
        print(subs)
        if subs:
            from jarvis.core_modules.network import Subscriber
            self.subs = {channel: {"": Subscriber(channel)} for channel in subs}
        if pubs:
            from jarvis.core_modules.network import Publisher
            self.pubs = {channel: Publisher(channel) for channel in pubs}
        if proxies:
            from jarvis.core_modules.network import Proxy
            self.proxies = {channel: Proxy(channel) for channel in proxies}
