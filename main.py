"""
Application entry point for Second Brain.

Initializes Qt application, creates the Python backend,
loads the QML user interface, exposes the backend to QML and configures
the system tray functionality.

Startup timings are printed to help identify performance bottlenecks.
"""

import time
startup_start = time.perf_counter()

import sys
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication,
    QSystemTrayIcon, 
    QMenu
)
from translator import Translator

from PySide6.QtGui import QIcon
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

# Give the application its own Windows taskbar identity.
if sys.platform == "win32":
    import ctypes

    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
        "SecondBrain.Desktop"
    )

# Start Qt application and create the engine that loads QML.
app = QApplication(sys.argv)

# Load the shared application icon.
icon_path = Path(__file__).resolve().parent / "assets" / "logo4.png"
icon = QIcon(str(icon_path))
app.setWindowIcon(icon)

engine = QQmlApplicationEngine()

backend_start = time.perf_counter()
backend = Backend()
backend_end = time.perf_counter()
print(f"Backend creation: {backend_end - backend_start:.3f} seconds")

# Make the Python object available to QML under the name "backend".
engine.rootContext().setContextProperty("backend", backend)

# Create translator object and expose it to QML.
translator = Translator(engine)
engine.rootContext().setContextProperty("translator", translator)

# Locate the QML entry file qml/main.qml
qml_file = Path(__file__).resolve().parent / "qml" / "main.qml"
qml_start = time.perf_counter()
engine.load(str(qml_file))
qml_end = time.perf_counter()
print(f"QML load: {qml_end - qml_start:.3f} seconds")

# Exit with an error code if the QML window could not be created.
if not engine.rootObjects():
    sys.exit(1)

# Get the main window that QML created and set its icon.
window = engine.rootObjects()[0]
window.setIcon(icon)

# Let the process continue even when the main window is closed.
app.setQuitOnLastWindowClosed(False)


def show_window() -> None:
    """
    Restore and activate the main application window.
    """

    window.showNormal()
    window.raise_()
    window.requestActivate()

# Use the application icon for the system tray.
tray_icon = QSystemTrayIcon(icon, app)
tray_icon.setToolTip("Second Brain")

# Create the tray icon menu.
tray_menu = QMenu()

open_action = tray_menu.addAction("")
open_action.triggered.connect(show_window)

quit_action = tray_menu.addAction("")
quit_action.triggered.connect(app.quit)


def update_tray_menu() -> None:
    """Update tray menu labels using the current interface language."""
    open_action.setText(
        translator.text("tray.open", translator.language)
    )
    quit_action.setText(
        translator.text("tray.quit", translator.language)
    )


translator.languageChanged.connect(update_tray_menu)
update_tray_menu()


tray_icon.setContextMenu(tray_menu)
tray_icon.show()

startup_end = time.perf_counter()

print(
    f"Total application startup: "
    f"{startup_end - startup_start:.3f} seconds"
)

# Keep the app running until the user selects Exit from the tray menu.
sys.exit(app.exec())