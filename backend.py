"""
Backend för applikationen.

Tänkt ansvar:
- kommunikation mellan QML och Python
- ta emot användarinput från gränssnittet
- skicka resultat tillbaka till QML

Exakt struktur bestäms under projektets gång.
"""
import sqlite3

from PySide6.QtCore import QObject, Signal, Slot, QUrl

from retrieval import retrieve_knowledge, create_embedding
from llm.local_provider import LocalLLMProvider
from performance import measure_time
from database import get_all_knowledge, add_knowledge, search_knowledge, edit_knowledge, delete_knowledge
from datetime import datetime
from pathlib import Path


class Backend(QObject):

    def __init__(self):
        super().__init__()
        # lighter and faster model
        self.llm = LocalLLMProvider("Qwen/Qwen3-0.6B")
        
        # more demanding model
        # self.llm = LocalLLMProvider("Qwen/Qwen3-4B-Instruct-2507")

    # Signal från Python till QML med texten som ska visas.
    replyReady = Signal(str)

    knowledgeLoaded = Signal(list)
    knowledgeSaveResult = Signal(str)

    # Send the edit result to QML.
    # Bool is used to check whether saving succeeded.
    knowledgeEditResult = Signal(bool, str)

    # Send the deletion result to QML.
    knowledgeDeleteResult = Signal(bool, str)

    # QML anropar denna metod och skickar med texten från användaren.
    @Slot(str)
    @measure_time
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

        # no_think to remove thinking mode from model
        prompt = f"""
    /no_think
    
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

    @Slot()
    def load_all_knowledge(self):
        '''
        Get all knowledge from database and send it to QML as a dictionary
        '''
        knowledge = get_all_knowledge()

        knowledge_data = []
        for item in knowledge:
            # format created at to: "YYYY-MM-DD H-M"
            created_at = datetime.fromisoformat(item["created_at"])
            formatted_created_at = created_at.strftime("%Y-%m-%d %H:%M")
            knowledge_data.append({
                "id": item["id"],
                "text": item["text"],
                "source": item["source"],
                "created_at": formatted_created_at
            })

        self.knowledgeLoaded.emit(knowledge_data)

    @Slot(str)
    def search_saved_knowledge(self, search):
        """Find posts matching the text or source and send them to QML."""
        search = search.strip()

        # Show all posts when the search field is empty.
        if not search:
            self.load_all_knowledge()
            return

        knowledge = search_knowledge(search)

        knowledge_data = []
        for item in knowledge:
            created_at = datetime.fromisoformat(item["created_at"])

            knowledge_data.append({
                "id": item["id"],
                "text": item["text"],
                "source": item["source"],
                "created_at": created_at.strftime("%Y-%m-%d %H:%M")
            })

        self.knowledgeLoaded.emit(knowledge_data)

    @Slot(int, str)
    def edit_saved_knowledge(self, knowledge_id, new_text):
        """Update a post and its embedding."""
        new_text = new_text.strip()

        # Reject empty text.
        if not new_text:
            self.knowledgeEditResult.emit(
                False, "Texten får inte vara tom."
            )
            return

        # Create an embedding that matches the updated text.
        embedding = create_embedding(new_text)

        try:
            updated = edit_knowledge(
                knowledge_id, new_text, embedding
            )
        except sqlite3.IntegrityError:
            self.knowledgeEditResult.emit(
                False, "Det finns redan en post med samma text."
            )
            return

        if updated:
            self.knowledgeEditResult.emit(
                True, "Kunskapsposten har uppdaterats."
            )
        else:
            self.knowledgeEditResult.emit(
                False, "Kunskapsposten kunde inte hittas."
            )

    @Slot(int)
    def delete_saved_knowledge(self, knowledge_id):
        """Delete the selected knowledge post."""
        deleted = delete_knowledge(knowledge_id)

        if deleted:
            self.knowledgeDeleteResult.emit(
                True, "Kunskapsposten har tagits bort."
            )
        else:
            self.knowledgeDeleteResult.emit(
                False, "Kunskapsposten kunde inte hittas."
            )
    
    @Slot (str)
    def add_manual_knowledge(self, text):
        '''
        Receives text from QML and if not empty,
        embeds the text and adds it to the knowledge database
        '''
        if not text.strip():
            self.knowledgeSaveResult.emit("No knowledge was added.")
            return

        embedding = create_embedding(text)

        added = add_knowledge(
            text, 
            embedding,
            source="manual"
        )

        if added:
            self.knowledgeSaveResult.emit("Knowledge added.")
        else:
            self.knowledgeSaveResult.emit("No new knowledge was added.")

    @Slot(str)
    def add_txt_knowledge(self, file_path):
        local_path = QUrl(file_path).toLocalFile() # convert to local windows file path
        path = Path(local_path)
        text = path.read_text(encoding="utf-8")

        # sort the text into chunks if text can be split into paragraphs
        chunks = [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]

        added_count = 0

        # create embeddings
        for chunk in chunks:
            embedding = create_embedding(chunk)
            # commit to db
            added = add_knowledge(chunk, embedding, source=path.name)
            if added: added_count += 1

        if added_count == 0:
            self.knowledgeSaveResult.emit("No new knowledge was added.")
        else:
            self.knowledgeSaveResult.emit("Text file imported.")
