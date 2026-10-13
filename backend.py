"""
Backend för applikationen.

Tänkt ansvar:
- kommunikation mellan QML och Python
- ta emot användarinput från gränssnittet
- skicka resultat tillbaka till QML

Exakt struktur bestäms under projektets gång.
"""
import sqlite3

from PySide6.QtCore import QObject, Signal, Slot, QUrl, QThread

from retrieval import retrieve_knowledge, create_embedding
from llm.local_provider import LocalLLMProvider
from performance import measure_time
from database import get_all_knowledge, add_knowledge, search_knowledge, edit_knowledge, delete_knowledge, initialize_database
from datetime import datetime
from pathlib import Path


class Thinker(QThread):
    """Process a question without blocking the interface."""

    answerReady = Signal(str)
    answerFailed = Signal(str)

    def __init__(self, llm, question):
        super().__init__()
        self.llm = llm
        self.question = question

    def run(self):
        try:
            results = retrieve_knowledge(self.question)

            if not results:
                self.answerReady.emit(
                    "Det finns inte tillräcklig information i kunskapsbasen."
                )
                return

            context = "\n".join(
                result["text"] for result in results
            )

            prompt = f"""
Use only the information in the context below to answer the question.

Rules:
- Answer only using information from the context.
- If the answer is not available in the context, say so clearly.
- Do not make up information.

CONTEXT:
{context}

QUESTION:
{self.question}

ANSWER:
"""

            answer = self.llm.generate(prompt)
            self.answerReady.emit(answer)

        except Exception as error:
            print(f"Answer generation failed: {error}")
            self.answerFailed.emit(
                "Svaret kunde inte skapas. Försök igen."
            )

class Backend(QObject):

    def __init__(self):
        super().__init__()

        # Keep a reference to the background thread.
        self.thinker = None

        initialize_database()

        # lighter and faster model
        # self.llm = LocalLLMProvider("Qwen/Qwen3-0.6B")

        # medium model
        self.llm = LocalLLMProvider("Qwen/Qwen3-1.7B")
        
        # more demanding model
        # self.llm = LocalLLMProvider("Qwen/Qwen3-4B-Instruct-2507")

    # Signal från Python till QML med texten som ska visas.
    replyReady = Signal(str)

    # Send True when processing starts and False when it finishes.
    thinkingChanged = Signal(bool)

    # Send an error message to QML.
    replyFailed = Signal(str)

    knowledgeLoaded = Signal(list)
    knowledgeSaveResult = Signal(str)

    # Send the edit result to QML.
    # Bool is used to check whether saving succeeded.
    knowledgeEditResult = Signal(bool, str)

    # Send the deletion result to QML.
    knowledgeDeleteResult = Signal(bool, str)

    @Slot(str)
    def receive_text(self, text):
        """Start processing a question in the background."""
        text = text.strip()

        # Ignore empty questions or requests while already processing.
        if not text or self.thinker is not None:
            return

        self.thinker = Thinker(self.llm, text)

        # Receive the answer, errors and notification that the thread ended.
        self.thinker.answerReady.connect(self.handle_answer)
        self.thinker.answerFailed.connect(self.handle_error)
        self.thinker.finished.connect(self.finish_thinking)

        # Show the thinking indicator and start the background work.
        self.thinkingChanged.emit(True)
        self.thinker.start()

    @Slot(str)
    def handle_answer(self, answer):
        """Send the answer to QML."""
        self.replyReady.emit(answer)

    @Slot(str)
    def handle_error(self, message):
        """Send the error message to QML."""
        self.replyFailed.emit(message)

    @Slot()
    def finish_thinking(self):
        """Clean up after the background thread has finished."""
        self.thinker.deleteLater()
        self.thinker = None
        self.thinkingChanged.emit(False)

    @Slot(str)
    def load_all_knowledge(self, sort_order="desc"):
        '''
        Get all knowledge from database and send it to QML as a dictionary
        '''
        knowledge = get_all_knowledge(sort_order)

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
        '''
        Receives a txt file from QML, and after passing safeguards, 
        splits it into chunks and adds them to the database.
        '''
        local_path = QUrl(file_path).toLocalFile() # convert to local windows file path
        path = Path(local_path)

        # safeguards
        if path.suffix.lower() != ".txt":
            self.knowledgeSaveResult.emit("Only .txt files are supported.")
            return
        if not path.exists():
            self.knowledgeSaveResult.emit("The selected file does not exist.")
            return
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            self.knowledgeSaveResult.emit("The file could not be read as UTF-8.") # catch unicode errors
            return
        except OSError:
            self.knowledgeSaveResult.emit("The file could not be read.")
            return
        if not text.strip():
            self.knowledgeSaveResult.emit("The file is empty.")
            return
        
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
            self.knowledgeSaveResult.emit(f"Imported {added_count} knowledge entries from text file.")