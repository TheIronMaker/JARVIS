from PySide6 import QtGui

def app_format(config: dict):
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
