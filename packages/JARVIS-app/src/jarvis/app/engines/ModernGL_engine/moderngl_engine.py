import moderngl
from pathlib import Path

from PySide6 import QtGui, QtOpenGLWidgets
from PySide6.QtCore import Qt

from jarvis.app.tools.simple_app import SimpleApp
from jarvis.core_modules.files import PathResolver
from jarvis.core.utils.collections import deep_merge

class ModernGLWidget(QtOpenGLWidgets.QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Removes window background color (default bright blue)
        self.setAttribute(Qt.WidgetAttribute.WA_AlwaysStackOnTop)
        self.ctx = None

    def initializeGL(self):
        self.ctx = moderngl.create_context()

        # Transparent Window - None of these were required... Maybe while rendering?
        self.ctx.enable(moderngl.BLEND)
        self.ctx.blend_func = (moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA)
        self.ctx.disable(moderngl.GL_DEPTH_TEST)

    def resizeGL(self, w, h):
        if self.ctx:
            self.ctx.viewport = (0, 0, w, h)

    def paintGL(self):
        if not self.ctx:
            return

        self.ctx.screen.use()
        self.ctx.clear(0.035, 0.118, 0.149, 0.2)

        # --- ModernGL rendering code goes here - e.g. vao---


def app_fmt(config: dict):
    if not config: return

    profiles = {
        "CoreProfile": QtGui.QSurfaceFormat.OpenGLContextProfile.CoreProfile,
        "CompatibilityProfile": QtGui.QSurfaceFormat.OpenGLContextProfile.CompatibilityProfile,
        "NoProfile": QtGui.QSurfaceFormat.OpenGLContextProfile.NoProfile
    }

    options = {
        "DeprecatedFunctions": QtGui.QSurfaceFormat.FormatOption.DeprecatedFunctions,
        "DebugContext": QtGui.QSurfaceFormat.FormatOption.DebugContext,
        "ResetNotification": QtGui.QSurfaceFormat.FormatOption.ResetNotification,
        "StereoBuffers": QtGui.QSurfaceFormat.FormatOption.StereoBuffers
    }

    fmt = QtGui.QSurfaceFormat()
    fmt.setVersion(*config["version"])
    fmt.setProfile(profiles.get(config["profile"], profiles["CoreProfile"]))
    
    options = config.get("options")
    #options = [] if options is None else [options] if isinstance(options, str) else options
    for opt in options: fmt.setOption(getattr(QtGui.QSurfaceFormat.FormatOption, opt))
    
    if type(config["transparency"]["alpha_buffer"]) == int:
        fmt.setAlphaBufferSize(config["transparency"]["alpha_buffer"])
    
    QtGui.QSurfaceFormat.setDefaultFormat(fmt)

if __name__ == "__main__":
    path = Path(__file__).parent / "config"

    app_config = PathResolver().load_file("main", "yaml", "config", "app/builds")
    default_config = PathResolver().load_file("fmt-base", "yaml", "project", path)
    config = deep_merge(default_config, app_config)
    
    config["main_window"]["ui_layout"]["central_widget"] = ModernGLWidget

    app_fmt(config.get("fmt"))
    app = SimpleApp(config)
    app.launch()