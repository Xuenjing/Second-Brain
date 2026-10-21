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

from retrieval import (
    retrieve_knowledge,
    create_embedding,
    get_embedding_model
)
from llm.local_provider import LocalLLMProvider
from database import (
    get_all_knowledge,
    get_knowledge_by_id,
    add_knowledge, 
    search_knowledge, 
    edit_knowledge, 
    delete_knowledge, 
    initialize_database
)
from imports.document_importer import import_docx_to_database
from imports.pdf_importer import import_pdf_to_database
from imports.text_importer import import_txt_to_database
from imports.mail_importer import import_mail_to_database
from exporter import export_knowledge_to_json



class Thinker(QThread):
    """Process a question without blocking the interface."""

    answerReady = Signal(str, list)
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
- Pay close attention to negation such as "not", "no", "does not", "inte", "inget" and "har inte".
- If the context explicitly states that something is not true, do not answer that it is true.
- Base the answer on the complete relevant statement, not only on matching words.
- Identify the statement in the context that refers to the same person or entity as the question.
- Answer strictly according to that statement.
- Do not infer information about one person or entity from information about another.
- The context may contain information that is related to the topic but does not answer the question.
- If the context does not explicitly contain the information needed to answer the question, respond that there is not enough information in the knowledge base.
- Answer in the same language as the question.
- Do not make up information.

CONTEXT:
{context}

QUESTION:
{self.question}

ANSWER:
"""

            answer = self.llm.generate(prompt)
            self.answerReady.emit(answer, results)

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

        # Preload embedding model during application startup.
        get_embedding_model()

        # lighter and faster model
        # self.llm = LocalLLMProvider("Qwen/Qwen3-0.6B")

        # medium model
        self.llm = LocalLLMProvider("Qwen/Qwen3-1.7B")
        
        # more demanding model
        # self.llm = LocalLLMProvider("Qwen/Qwen3-4B-Instruct-2507")

    # Signal from Python to QML with the text to display.
    replyReady = Signal(str, list)

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

    # Send the id of the clicked post to QML
    knowledgeEntryOpened = Signal(int, str, str, str)

    # Backup the database to a JSON file.
    exportResult = Signal(str)

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

    @Slot(str, list)
    def handle_answer(self, answer: str, sources: list) -> None:
        """Send the answer to QML.
        
        Args:
            answer: generated answer to display in QML interface.
        """
        self.replyReady.emit(answer, sources)

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
        """Import knowledge from a UTF-8 text file.

            Args:
                file_path: File URL received from the QML.
        """

        # convert to local windows file path
        local_path = QUrl(file_path).toLocalFile() 

        try:
            added_count = import_txt_to_database(local_path)
        except FileNotFoundError:
            self.knowledgeSaveResult.emit("The selected file does not exist")
            return
        except ValueError as error:
            self.knowledgeSaveResult.emit(str(error))
            return
        
        if added_count == 0:
            self.knowledgeSaveResult.emit("No new knowledge was added.")
        else:
            self.knowledgeSaveResult.emit(
                f"Imported {added_count} knowledge entries from text file."
            )


    @Slot(str)
    def add_docx_knowledge(self, file_path: str) -> None:
        """Import knowledge from a DOCX file.

        Args:
            file_path: File URL received from QML.
        """

        local_path = QUrl(file_path).toLocalFile()

        try:
            added_count = import_docx_to_database(local_path)
        except (FileNotFoundError, ValueError) as error:
            self.knowledgeSaveResult.emit(str(error))
            return

        if added_count == 0:
            self.knowledgeSaveResult.emit("No new knowledge was added.")
        else:
            self.knowledgeSaveResult.emit(f"Imported {added_count} knowledge entries from docx file.")


    @Slot(str)
    def add_pdf_knowledge(self, file_path: str) -> None:
        """Import knowledge from a PDF file.
        
        Args:
            file_path: File URL received from QML.
        """

        local_path = QUrl(file_path).toLocalFile()

        try:
            added_count = import_pdf_to_database(local_path)
        except (FileNotFoundError, ValueError) as error:
            self.knowledgeSaveResult.emit(str(error))
            return

        if added_count == 0:
            self.knowledgeSaveResult.emit("No new knowledge was added")
        else:
            self.knowledgeSaveResult.emit(f"Imported {added_count} knowledge entries from pdf file.")

    @Slot(str)
    def add_mail_knowledge(self, file_path: str) -> None:
        """Import knowledge from an EML file.

        Args:
            file_path: File URL received from QML.

        Returns:
            None.
        """
        # Convert the file URL to a local file path.
        local_path = QUrl(file_path).toLocalFile()

        try:
            added_count = import_mail_to_database(local_path)
        except FileNotFoundError:
            self.knowledgeSaveResult.emit(
                "The selected file does not exist."
            )
            return
        except ValueError as error:
            self.knowledgeSaveResult.emit(str(error))
            return
        except OSError:
            self.knowledgeSaveResult.emit(
                "The file could not be read."
            )
            return

        if added_count == 0:
            self.knowledgeSaveResult.emit("No new knowledge was added.")
        else:
            self.knowledgeSaveResult.emit(
                f"Imported {added_count} knowledge entries from EML file."
            )


    @Slot(str, str, bool, bool, bool, bool)
    def load_filtered_knowledge(self,
        search: str, 
        sort_order: str, 
        txt_active: bool, 
        docx_active: bool, 
        pdf_active: bool, 
        manual_active: bool
    ) -> None:
        """Load and filter knowledge for display in QML.
        
        Args:
            search: Search text matched against stored knowledge (text and source).
            sort_order: Sort order by creation time.
            txt_active: Whether TXT entries should be included or not.
            docx_active. Whether DOCX entries should be included or not.
            pdf_active: Whether PDF entries should be included or not.
            manual_active: whether manual entries should be included or not.
        """
        search = search.strip()

        if search:
            knowledge = search_knowledge(search)
        else:
            knowledge = get_all_knowledge(sort_order)

        reverse = sort_order == "desc"

        knowledge.sort(key=lambda item: item["created_at"], reverse=reverse)

        filtered_knowledge = []

        for item in knowledge:
            source = item["source"].lower()

            if txt_active and source.endswith(".txt"):
                filtered_knowledge.append(item)
            elif docx_active and source.endswith(".docx"):
                filtered_knowledge.append(item)
            elif pdf_active and source.endswith(".pdf"):
                filtered_knowledge.append(item)
            elif manual_active and source == "manual":
                filtered_knowledge.append(item)

        knowledge_data = self._format_knowledge_for_qml(filtered_knowledge)
        self.knowledgeLoaded.emit(knowledge_data)


    def _format_knowledge_for_qml(self, knowledge: list[dict]) -> list[dict]:
        """Format knowledge entries for display in QML.

        Internal helper function, not called by QML directly.
        
        Args:
            knowledge: Knowledge entries from database.

        Returns:
            Knowledge entries formatted for QML.
        """

        knowledge_data = []

        for item in knowledge:
            created_at = datetime.fromisoformat(item["created_at"])

            knowledge_data.append({
                "id": item["id"],
                "text": item["text"],
                "source": item["source"],
                "created_at": created_at.strftime("%Y-%m-%d %H:%M")
            })

        return knowledge_data
    

    @Slot(int)
    def open_knowledge_entry(self, knowledge_id: int) -> None:
        """Send a selected knowledge entry to QML.
        
            Args:
                knowledge_id: Database ID of the knowledge entry.
        """

        item = get_knowledge_by_id(knowledge_id)

        created_at = datetime.fromisoformat(item["created_at"]).strftime("%Y-%m-%d %H:%M")

        self.knowledgeEntryOpened.emit(
            item["id"],
            item["text"],
            item["source"],
            created_at
        )
        return


    @Slot(str)
    def export_knowledge(self, file_path: str) -> None:
        """Export all knowledge entries to a JSON file.
        
            Args:
                file_path: Destination file URL received from QML.
        """

        # Translate working file path between QML and Python.
        local_path = QUrl(file_path).toLocalFile()

        try:
            exported_count = export_knowledge_to_json(local_path)
        except OSError:
            self.exportResult.emit("The knowledge could not be exported.")
            return

        self.exportResult.emit(
            f"Exported {exported_count} knowledge entries."
        )