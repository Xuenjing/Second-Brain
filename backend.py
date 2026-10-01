"""
Backend för applikationen.

Tänkt ansvar:
- kommunikation mellan QML och Python
- ta emot användarinput från gränssnittet
- skicka resultat tillbaka till QML

Exakt struktur bestäms under projektets gång.
"""

from PySide6.QtCore import QObject, Signal, Slot

from retrieval import retrieve_knowledge
from llm.local_provider import LocalLLMProvider


class Backend(QObject):

    def __init__(self):
        super().__init__()

        self.llm = LocalLLMProvider(
            "Qwen/Qwen3-4B-Instruct-2507"
            )

    # Signal från Python till QML med texten som ska visas.
    replyReady = Signal(str)

    # QML anropar denna metod och skickar med texten från användaren.
    @Slot(str)
    def receive_text(self, text):
        # Sök efter kunskap som matchar frågan från QML.
        results = retrieve_knowledge(text)

        if not results:
            self.replyReady.emit(
                "Det finns inte tillräcklig information i kunskapsbasen."
                )
            return

        # Visa träffarna i terminalen för kontroll.
        print("Retrieved:")
        for result in results:
            print(result)

        context = "\n".join(
            result["text"]
            for result in results
        )

        prompt = f"""
    Use only the information in the context below to answer the question.

    CONTEXT:
    {context}

    QUESTION:
    {text}

    ANSWER:
    """

        answer = self.llm.generate(prompt)

        # Bekräfta i gränssnittet att anropet har körts.
        self.replyReady.emit(answer)