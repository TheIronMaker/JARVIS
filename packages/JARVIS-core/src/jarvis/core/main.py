from jarvis.core_modules.logger import Logger
from jarvis.core_modules.files import PathResolver
from jarvis.core_modules.threaded import ThreadedResource
from jarvis.core_modules.network import DataBus
from jarvis.app.app import app


class Old_Core(ThreadedResource):
    def __init__(self, id, parent_config=None):
        self.id = id
        self.parent_config = parent_config
        self.bus = DataBus()

        # Ideally, the id would be almost any type of data format a config could store.
        self.config = PathResolver.load_file(str(id), ".json", "project", "configs/core")
        super().__init__(self.config.get("cycle_time"))
    
        self.module_managers = {}
        #self.load_module_managers()

    def initialize(self):
        if self.config.get("start_thread"):
            self._start_thread()
        
        if self.config.get("run_method") == "terminal":
            self.main_process()
        elif self.config.get("run_method") == "app":
            app(self.bus) # This will take over the main thread - Later create a method to handle this
            # First code will not end until all cores are stopped, right now.
            # Biggest issue: cores start in succession of each other, since the app takes over main thread

    def load_module_managers(self):
        for manager_build in self.config.get("module_managers", []):
            if manager_build.get("enabled", True):
                id = manager_build.get("id")
                if not id:
                    
                    Logger.error("Module manager build missing id. Skipping.")
                    continue
                #manager = ModuleManager(self.bus, id)
                #manager.start_modules()
                #self.module_managers[id] = manager #@revisit-add: if id exists

    def _main_process(self):
        pass
    
    def _close(self):
        for module_manager in self.module_managers.values():
            module_manager.destruct()

def construct_cores(build):
    cores = {}
    for core_build in build.get("instances", []):
        id = core_build.get("id")
        if core_build.get("enabled") == False or not id:
            continue

        cores[id] = Old_Core(id)
    return cores

# The Core factory is not refined now
def old_main():
    build = PathResolver.load_file("core_main", ".json", "project", "configs/core")
    cores = construct_cores(build)
    for core in cores.values():
        core.initialize()
    
    # Stops main program after application closes - needs to track running cores and close them properly
    for core in cores.values():
        for module_manager in core.module_managers.values():
            module_manager.destruct()
        core._stop_thread()


class Core(ThreadedResource):
    def __init__(self, config):
        self.config = config
        super().__init__(config.get("cycle_time"))

def main() -> None:
    # Goal: Core class starts and manages itself
    # This may be improved by building a proper YAML parser/verification
    config = PathResolver.load_file(
        "core",
        ".yaml",
        "project",
        f"JARVIS/config.example/jarvis-core/builds/019fa242-4668-78ae-bd04-cd46330c858a")

    Core(config)

    # To be driven by config values
    window = app()

if __name__ == "__main__":
    main()