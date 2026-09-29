"""
Backend för applikationen.

Tänkt ansvar:
- kommunikation mellan QML och Python
- ta emot användarinput från gränssnittet
- skicka resultat tillbaka till QML

Exakt struktur bestäms under projektets gång.
"""

from PySide6.QtCore import QObject, Signal, Slot


class Backend(QObject):
    # Signal från Python till QML med texten som ska visas.
    replyReady = Signal(str)

    # QML anropar denna metod och skickar med texten från användaren.
    @Slot(str)
    def receive_text(self, text):
        reply = f"Mottaget: {text}"
        self.replyReady.emit(reply)