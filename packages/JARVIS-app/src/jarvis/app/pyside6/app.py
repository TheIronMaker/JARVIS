import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QLabel, QDockWidget, QSizePolicy
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt, QTimer

from jarvis.app.pyside6.view_container import ViewContainer
from jarvis.core_modules.files import PathResolver

CONFIG_PATH = "JARVIS/config.example/jarvis-app/app/builds"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.build = PathResolver.load_file("app", ".yaml", "project", "JARVIS/config.example/jarvis-app/app/builds/019fa25d-06c3-7cec-b5ff-4400e131ab13")
        self.view_managers = {}
        self.docks = {}

        #self.load_view_managers()
        #self._build_central()
    
    def load_view_managers(self):
        for config in self.build.get("view_managers", []):
            if not config.get("enabled", True):
                continue
            name = config.get("name")
            self.view_managers[name] = ViewContainer(self, config)

    def _build_central(self):
        self.setWindowTitle("JARVIS")
        self.setDockOptions(QMainWindow.AllowTabbedDocks)
        central = QWidget()
        layout = QHBoxLayout() # Will need config driven approach

        self.workspace = QLabel("Main workspace")
        self.workspace.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Will need to add layout configurations and more complex stacking options through config files
        for view_manager in self.view_managers.values():
            view_stack = view_manager.stack()
            if view_stack:
                #view_stack.addWidget(self.workspace)
                layout.addLayout(view_stack)

        layout.setContentsMargins(0, 0, 0, 0)
        central.setLayout(layout)
        self.setCentralWidget(central)

    def add_dock(self, name, widget, dock_area="right", initial_size=300):
        area = {
            "left": Qt.LeftDockWidgetArea,
            "right": Qt.RightDockWidgetArea,
            "top": Qt.TopDockWidgetArea,
            "bottom": Qt.BottomDockWidgetArea,
        }.get(dock_area, Qt.RightDockWidgetArea)

        dock = QDockWidget(name.capitalize(), self)
        dock.setWidget(widget)
        dock.setAllowedAreas(Qt.AllDockWidgetAreas)
        self.addDockWidget(area, dock)

        orientation = Qt.Horizontal if dock_area in ("left", "right") else Qt.Vertical
        self.resizeDocks([dock], [initial_size], orientation)
        self.docks[name] = dock
    
    def paintEvent(self, event):
        """ Handles all paint events. PySide6 painter may only be used within this function """
        with QPainter(self) as painter:
            for view_manager in self.view_managers.values():
                view_manager.paint_views(event, painter)
    
    def keyPressEvent(self, event):
        for view_manager in self.view_managers.values():
            view_manager.keyPressEvent(event)



def run_boot(instructions):
    import importlib
    for import_path, config in instructions.get("boot_operations").items():
        cls = importlib.import_module(import_path)
        for function_name, function_config in config.get("functions").items():
            callable_func = getattr(cls, function_name)
            if not callable(callable_func):
                raise TypeError(f"'{function_name}' in {import_path} is not a function.")

            callable_func(function_config)

def app(*args):
    boot_instructions = PathResolver.load_file("boot", "yaml", "project", CONFIG_PATH)
    run_boot(boot_instructions)

    # manifest = PathResolver.load_file("manifest", "json", "project", CONFIG_PATH)
    # for node_id, config in manifest.get("nodes", []).items():
    #     node_config = PathResolver.load_file(str(node_id) + "/app", "yaml", "project", config_path)

    app = QApplication(sys.argv)
    window = MainWindow(*args)
    window.resize(1200, 800)
    window.show()

    timer = QTimer()
    timer.setInterval(10)
    for view_manager in window.view_managers.values():
        timer.timeout.connect(view_manager.update)
    timer.start()

    app.exec()

if __name__ == "__main__":
    app()