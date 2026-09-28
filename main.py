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

import sys
from pathlib import Path

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine


# Starta Qt-applikationen och skapa motorn som läser QML.
app = QGuiApplication(sys.argv)
engine = QQmlApplicationEngine()

# Hitta qml/main.qml
qml_file = Path(__file__).resolve().parent / "qml" / "main.qml"
engine.load(str(qml_file))

# Avsluta med ett fel om QML-fönstret inte kunde skapas.
if not engine.rootObjects():
    sys.exit(1)

# Håll appen igång tills användaren stänger fönstret.
sys.exit(app.exec())