
from jarvis.core_modules.files import PathResolver
from jarvis.core_modules.threaded import ThreadedResource
from jarvis.app.pyside6.app import app


class Core:
    def __init__(self, core_id):
        self.config = PathResolver.load_file("core", "yaml", "project", f"JARVIS/config.example/jarvis-core/builds/{core_id}")

class ThreadedCore(Core, ThreadedResource):
    def __init__(self, core_id,):
        super().__init__(core_id)

def main():
    manifest = PathResolver.load_file(
            "manifest",
            "json",
            "project",
            f"JARVIS/config.example/jarvis-core/builds")

    # Load cores
    cores = {}
    for core_id, config in manifest.get("nodes", []).items():
        cls = ThreadedCore if config.get("threaded") else Core
        cores[core_id] = cls(core_id)

    app()

if __name__ == "__main__":
    main()
