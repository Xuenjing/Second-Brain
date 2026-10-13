'''
Application entry point for Second Brain.

Initializes Qt application, creates the Python backend,
loads the QML user interface, exposes the backend to QML and configures
the system tray functionality.

Startup timings are printed to help identify performance bottlenecks.
'''

import time
startup_start = time.perf_counter()

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QStyle
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuickControls2 import QQuickStyle

backend_import_start = time.perf_counter()
from backend import Backend
backend_import_end = time.perf_counter()

print(
    f"Backend import: "
    f"{backend_import_end - backend_import_start:.3f} seconds"
)

# Use a style that supports custom QML controls.
QQuickStyle.setStyle("Basic")

# Start Qt application and create the engine that loads QML.
app = QApplication(sys.argv)
engine = QQmlApplicationEngine()

backend_start = time.perf_counter()
backend = Backend()
backend_end = time.perf_counter()
print(f"Backend creation: {backend_end - backend_start:.3f} seconds")

# Make the Python object available to QML under the name "backend". 
engine.rootContext().setContextProperty("backend", backend)

# Find qml/main.qml
qml_file = Path(__file__).resolve().parent / "qml" / "main.qml"
qml_start = time.perf_counter()
engine.load(str(qml_file))
qml_end = time.perf_counter()
print(f"QML load: {qml_end - qml_start:.3f} seconds")

# Exit with an error code if the QML window could not be created.
if not engine.rootObjects():
    sys.exit(1)

# Get the main window that QML created.
window = engine.rootObjects()[0]

# Let the process continue even when the main window is closed. 
app.setQuitOnLastWindowClosed(False)

def show_window() -> None:
    '''
    Restore and activate the main application window.
    '''
    window.showNormal()
    window.raise_()
    window.requestActivate()

# Use a built-in Qt icon until we choose our own.
icon = app.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)
tray_icon = QSystemTrayIcon(icon, app)
tray_icon.setToolTip("Second Brain")

# Right click menu for the tray icon.
tray_menu = QMenu()

open_action = tray_menu.addAction("Öppna")
open_action.triggered.connect(show_window)

quit_action = tray_menu.addAction("Avsluta")

def quit_application() -> None:
    """Cancel ongoing work and wait before closing the app."""
    thinker = backend.thinker

    if thinker is not None:
        quit_action.setEnabled(False)
        backend.cancel_question()
        thinker.wait()

    app.quit()

quit_action.triggered.connect(quit_application)

tray_icon.setContextMenu(tray_menu)
tray_icon.show()

startup_end = time.perf_counter()

print(
    f"Total application startup: "
    f"{startup_end - startup_start:.3f} seconds"
)

# Keep the app running until the user selects Exit from the tray menu.
sys.exit(app.exec())