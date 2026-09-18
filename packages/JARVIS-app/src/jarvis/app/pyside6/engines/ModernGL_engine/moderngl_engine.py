import moderngl
from pathlib import Path

from PySide6 import QtOpenGLWidgets
from PySide6.QtCore import Qt

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
