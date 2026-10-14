"""
Backend layer for the Second Brain application.

This module handles communication between QML and Python, manages
knowledge-base operations, and coordinates language-model generation
in a background thread.
"""

import sqlite3
from datetime import datetime
from pathlib import Path

from PySide6.QtCore import QObject, Signal, Slot, QUrl, QThread

from retrieval import retrieve_knowledge, create_embedding
from llm.local_provider import LocalLLMProvider
from database import (
    get_all_knowledge,
    add_knowledge, 
    search_knowledge, 
    edit_knowledge, 
    delete_knowledge, 
    initialize_database
)



class Thinker(QThread):
    """Process a question without blocking the interface."""

    answerReady = Signal(str)
    answerFailed = Signal(str)

    def __init__(self, llm: LocalLLMProvider, question: str) -> None:
        """Initialize a background question-processing thread.

        Args:
            llm: Language-model provider used to generate the answer.
            question: User question.
        """
        super().__init__()
        self.llm = llm
        self.question = question

    def run(self) -> None:
        """Retrieve relevant knowledge and generate an answer."""

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
    """Handle communication between QML and application."""

    def __init__(self) -> None:
        """Initialize the database, backend and local language model."""
        super().__init__()

        # Keep a reference to the background thread.
        self.thinker: Thinker | None = None

        initialize_database()

        # lighter and faster model
        # self.llm = LocalLLMProvider("Qwen/Qwen3-0.6B")

        # medium model
        self.llm = LocalLLMProvider("Qwen/Qwen3-1.7B")
        
        # more demanding model
        # self.llm = LocalLLMProvider("Qwen/Qwen3-4B-Instruct-2507")

    # Signal from Python to QML with the text to display.
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
    def receive_text(self, text: str) -> None:
        """Start processing a question in the background.
        
        Args:
            text: question from the QML interface.
        """
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
    def handle_answer(self, answer: str) -> None:
        """Send the answer to QML.
        
        Args:
            answer: generated answer to display in QML interface.
        """
        self.replyReady.emit(answer)

    @Slot(str)
    def handle_error(self, message: str) -> None:
        """Send the error message to QML.
        
        Args:
            message: error message to display in QML interface.
        """
        self.replyFailed.emit(message)

    @Slot()
    def finish_thinking(self) -> None:
        """Clean up after the background thread has finished."""
        self.thinker.deleteLater()
        self.thinker = None
        self.thinkingChanged.emit(False)

    @Slot(str)
    def load_all_knowledge(self, sort_order: str = "desc") -> None:
        """
        Load stored knowledge and send it to QML.
        
        Args:
            sort_order: sort order for entries by creation time (ascending or descending).
        """
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
    def search_saved_knowledge(self, search: str) -> None:
        """Search stored entries and send matches to QML.
        
        Args:
            search: search term matched against stored text and source.
        """
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
    def edit_saved_knowledge(self, knowledge_id: int, new_text: str) -> None:
        """Update the text and embedding of an entry.
        
        Args:
            knowledge_id: Database ID of the entry.
            new_text: Replacement text for the entry.
        """
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
    def delete_saved_knowledge(self, knowledge_id: int) -> None:
        """Delete a knowledge entry.
        
        Args:
            knowledge_id: Database ID of the entry.
        """

        deleted = delete_knowledge(knowledge_id)

        if deleted:
            self.knowledgeDeleteResult.emit(
                True, "Kunskapsposten har tagits bort."
            )
        else:
            self.knowledgeDeleteResult.emit(
                False, "Kunskapsposten kunde inte hittas."
            )
    
    @Slot(str)
    def add_manual_knowledge(self, text: str) -> None:
        """
        Add manually added text to knowledge database.

        Args:
            text: knowledge text received from QML.
        """

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
    def add_txt_knowledge(self, file_path: str) -> None:
        """
        Import knowledge from a UTF-8 text file.

        The file is split into chunks based on paragraphs.
        Each chunk is embedded and stored separately in the database.

        Args:
            file_path: File URL received from the QML.
        """

        # convert to local windows file path
        local_path = QUrl(file_path).toLocalFile() 
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
            self.knowledgeSaveResult.emit("The file could not be read as UTF-8.")
            return
        except OSError:
            self.knowledgeSaveResult.emit("The file could not be read.")
            return
        if not text.strip():
            self.knowledgeSaveResult.emit("The file is empty.")
            return
        
        # sort the text into chunks if text can be split into paragraphs
        chunks = [
            chunk.strip()
            for chunk in text.split("\n\n") 
            if chunk.strip()
        ]

        added_count = 0

        for chunk in chunks:
            embedding = create_embedding(chunk)
            added = add_knowledge(chunk, embedding, source=path.name)
            if added:
                added_count += 1

        if added_count == 0:
            self.knowledgeSaveResult.emit("No new knowledge was added.")
        else:
            self.knowledgeSaveResult.emit(
                f"Imported {added_count} knowledge entries from text file."
            )