'''
Fusklapp 

QML → UI
PySide6 → kopplar Python till Qt/QML
Signal → Python skickar till QML
Slot → QML anropar Python
Embedding → text → vektor
Cosine similarity → jämför semantisk likhet
RAG → retrieval + context + LLM
SQLite → lagring
'''

import time
startup_start = time.perf_counter()

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QStyle
from PySide6.QtQml import QQmlApplicationEngine

from backend import Backend


# Starta Qt-applikationen och skapa motorn som läser QML.
app = QApplication(sys.argv)
engine = QQmlApplicationEngine()

# Gör Python-objektet tillgängligt i QML under namnet "backend".
backend = Backend()
engine.rootContext().setContextProperty("backend", backend)

# Hitta qml/main.qml
qml_file = Path(__file__).resolve().parent / "qml" / "main.qml"
engine.load(str(qml_file))

# Avsluta med ett fel om QML-fönstret inte kunde skapas.
if not engine.rootObjects():
    sys.exit(1)

# Hämta huvudfönstret som skapades av QML.
window = engine.rootObjects()[0]

# Låt processen fortsätta även när huvudfönstret stängs.
app.setQuitOnLastWindowClosed(False)

def show_window():
    window.showNormal()
    window.raise_()
    window.requestActivate()

# Använder en inbyggd Qt-ikon tillfälligt tills vi väljer en egen senare.
icon = app.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)
tray_icon = QSystemTrayIcon(icon, app)
tray_icon.setToolTip("Second Brain")

# Högerklicksmeny för tray-ikonen.
tray_menu = QMenu()

open_action = tray_menu.addAction("Öppna")
open_action.triggered.connect(show_window)

quit_action = tray_menu.addAction("Avsluta")
quit_action.triggered.connect(app.quit)

tray_icon.setContextMenu(tray_menu)
tray_icon.show()

startup_end = time.perf_counter()

print(
    f"Total application startup: "
    f"{startup_end - startup_start:.3f} seconds"
)

# Håll appen igång tills användaren väljer Avsluta i tray-menyn.
sys.exit(app.exec())