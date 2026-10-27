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
from imports.mail_parser import extract_mail_chunks
from imports.mail_fact_extractor import extract_mail_facts
from exporter import export_knowledge_to_json
from json_importer import import_knowledge_from_json_file



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
                    "Det finns inte tillräcklig information i kunskapsbasen.",
                    []
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

class ModelLoader(QThread):
    """Load a language model without blocking the interface."""

    modelLoaded = Signal(object)
    modelLoadFailed = Signal(str)

    def __init__(self, model_name: str) -> None:
        super().__init__()
        self.model_name = model_name

    def run(self) -> None:
        try:
            llm = LocalLLMProvider(self.model_name)
            self.modelLoaded.emit(llm)
        except Exception as error:
            print(f"Model loading failed: {error}")
            self.modelLoadFailed.emit(
                "Modellen kunde inte laddas."
            )

class MailFactWorker(QThread):
    """Suggest email facts without blocking the interface."""

    reviewReady = Signal(str, list, str)
    extractionFailed = Signal(str)

    def __init__(
        self,
        llm: LocalLLMProvider,
        email_text: str,
        source: str
    ) -> None:
        """Initialize the email-analysis thread.

        Args:
            llm: Loaded language-model provider.
            email_text: Previewed email text to analyze.
            source: Original email filename.
        """
        super().__init__()
        self.llm = llm
        self.email_text = email_text
        self.source = source

    def run(self) -> None:
        """Suggest facts and send them for manual review."""
        try:
            facts = extract_mail_facts(
                self.email_text,
                self.llm
            )

            self.reviewReady.emit(
                self.email_text,
                facts,
                self.source
            )
        except Exception as error:
            print(f"Email fact extraction failed: {error}")
            self.extractionFailed.emit(
                "Mejlet kunde inte analyseras. Försök igen."
            )
        
class Backend(QObject):
    """Handle communication between QML and application."""

    def __init__(self) -> None:
        """Initialize the database, backend and local language model."""
        super().__init__()

        # Keep a reference to the background thread.
        self.thinker: Thinker | None = None

        # Keep a reference to the model-loading thread.
        self.model_loader: ModelLoader | None = None

        # Keep the previewed email until the user chooses an action.
        self.mail_text: str = ""
        self.mail_source: str = ""

        # Keep a reference to the email-analysis thread.
        self.mail_worker: MailFactWorker | None = None

        # Keep the analysis result until the user reviews it.
        self.mail_review_text: str = ""
        self.mail_review_facts: list[str] = []
        self.mail_review_source: str = ""
        self.mail_review_pending: bool = False

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

    # Send True when changing a LLM.
    modelLoadingChanged = Signal(bool)

    # Send a message while the LLM is loading.
    modelLoadStatus = Signal(str)    

    # Send an error message to QML.
    replyFailed = Signal(str)

    knowledgeLoaded = Signal(list)
    knowledgeSaveResult = Signal(str)

    # Send the email text and filename to QML for preview.
    mailPreviewReady = Signal(str, str)

    # Notify QML when email analysis starts or finishes.
    mailAnalysisChanged = Signal(bool)

    # Notify QML when suggestions are available for review.
    mailReviewReady = Signal(str, list, str)

    # Notify QML when the review has been saved or discarded.
    mailReviewFinished = Signal()

    # Send the edit result to QML.
    # Bool is used to check whether saving succeeded.
    knowledgeEditResult = Signal(bool, str)

    # Send the deletion result to QML.
    knowledgeDeleteResult = Signal(bool, str)

    # Send the id of the clicked post to QML
    knowledgeEntryOpened = Signal(int, str, str, str)

    # Backup the database to a JSON file.
    exportResult = Signal(str)

    # Import JSON file from backup.
    importResult = Signal(str)

    @Slot(int)
    def load_model(self, model_index: str) -> None:
        """Load the language model selected from the interface.
        
            Args:
                model_index: Name of the model that will be loaded.
        """
        if self.thinker is not None or self.mail_worker is not None:
            self.modelLoadStatus.emit(
                "Vänta tills det pågående arbetet är klart."
            )
            return

        models = {
            0: "Qwen/Qwen3-0.6B",
            1: "Qwen/Qwen3-1.7B",
            2: "Qwen/Qwen3-4B-Instruct-2507"
        }

        model_name = models.get(model_index)

        if model_name is None:
            print(f"Invalid model index: {model_index}")
            return

        if model_name == self.llm.model_name:
            print("Model is already loaded")
            return

        if self.model_loader is not None:
            print("A model is already being loaded.")
            return

        self.model_loader = ModelLoader(model_name)

        self.model_loader.modelLoaded.connect(
            self.handle_model_loaded
        )

        self.model_loader.modelLoadFailed.connect(
            self.handle_model_load_error
        )

        self.model_loader.finished.connect(
            self.finish_model_loading
        )

        print(F"Requested model: {model_name}")

        self.modelLoadingChanged.emit(True)
        self.modelLoadStatus.emit(f"Laddar modell: {model_name}")

        self.model_loader.start()


    @Slot(object)
    def handle_model_loaded(self, llm: LocalLLMProvider) -> None:
        """Replace the current language model after successful loading."""

        self.llm = llm
        self.modelLoadStatus.emit(f"Modellen har laddats: {self.llm.model_name}")
        print(f"Model loaded {self.llm.model_name}")

    @Slot(str)
    def handle_model_load_error(self, message: str) -> None:
        """Handle errors that occur while loading a language model."""

        self.modelLoadStatus.emit(message)
        print(message)

    @Slot()
    def finish_model_loading(self) -> None:
        """Clean up after model loading has finished."""

        self.model_loader.deleteLater()
        self.model_loader = None

        self.modelLoadingChanged.emit(False)


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

        if self.mail_worker is not None or self.model_loader is not None:
            self.replyFailed.emit(
                "Modellen är upptagen. Vänta tills arbetet är klart."
            )
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
    def preview_mail(self, file_path: str) -> None:
        """Read an email for preview without saving it.

        Args:
            file_path: File URL received from QML.
        """
        # Clear any previously previewed email.
        self.mail_text = ""
        self.mail_source = ""

        local_path = QUrl(file_path).toLocalFile()

        try:
            chunks = extract_mail_chunks(local_path)
        except (FileNotFoundError, ValueError, OSError) as error:
            self.knowledgeSaveResult.emit(str(error))
            return

        self.mail_text = "\n\n".join(chunks)
        self.mail_source = Path(local_path).name

        self.mailPreviewReady.emit(
            self.mail_text,
            self.mail_source
        )

    @Slot()
    def save_previewed_mail(self) -> None:
        """Save the previewed email to the knowledge database."""
        if not self.mail_text.strip():
            self.knowledgeSaveResult.emit(
                "Det finns inget mejl att spara."
            )
            return

        try:
            embedding = create_embedding(self.mail_text)

            added = add_knowledge(
                self.mail_text,
                embedding,
                source=self.mail_source
            )
        except Exception as error:
            print(f"Saving email failed: {error}")
            self.knowledgeSaveResult.emit(
                "Mejlet kunde inte sparas. Försök igen."
            )
            return

        if added:
            self.knowledgeSaveResult.emit("Mejlet har sparats.")
        else:
            self.knowledgeSaveResult.emit(
                "Mejlet finns redan i kunskapsbasen."
            )
    @Slot()
    def analyze_previewed_mail(self) -> None:
        """Start background analysis of the previewed email."""
        if not self.mail_text.strip():
            self.knowledgeSaveResult.emit(
                "Det finns inget mejl att analysera."
            )
            return

        if (
            self.thinker is not None
            or self.model_loader is not None
            or self.mail_worker is not None
        ):
            self.knowledgeSaveResult.emit(
                "Vänta tills det pågående arbetet är klart."
            )
            return

        if self.mail_review_pending:
            self.knowledgeSaveResult.emit(
                "Granska eller kasta de tidigare förslagen först."
            )
            return

        self.mail_worker = MailFactWorker(
            self.llm,
            self.mail_text,
            self.mail_source
        )

        self.mail_worker.reviewReady.connect(self.handle_mail_review)
        self.mail_worker.extractionFailed.connect(self.handle_mail_error)
        self.mail_worker.finished.connect(self.finish_mail_analysis)

        self.knowledgeSaveResult.emit("Analyserar mejlet…")
        self.mailAnalysisChanged.emit(True)
        self.mail_worker.start()

    @Slot(str, list, str)
    def handle_mail_review(
        self,
        email_text: str,
        facts: list[str],
        source: str
    ) -> None:
        """Store email suggestions and notify the interface.

        Args:
            email_text: Original email text.
            facts: Suggested factual passages.
            source: Original email filename.
        """
        self.mail_review_text = email_text
        self.mail_review_facts = facts
        self.mail_review_source = source
        self.mail_review_pending = True

        self.knowledgeSaveResult.emit(
        "Mejlanalysen är klar. Granska förslagen innan du sparar."
    )

        self.mailReviewReady.emit(email_text, facts, source)

    @Slot()
    def reopen_mail_review(self) -> None:
        """Send pending email suggestions to the interface again."""
        if not self.mail_review_pending:
            self.knowledgeSaveResult.emit(
                "Det finns inga mejlförslag att granska."
            )
            return

        self.mailReviewReady.emit(
            self.mail_review_text,
            self.mail_review_facts,
            self.mail_review_source
        )

    @Slot(str)
    def handle_mail_error(self, message: str) -> None:
        """Display an email-analysis error.

        Args:
            message: Error message to display.
        """
        self.knowledgeSaveResult.emit(message)


    @Slot()
    def finish_mail_analysis(self) -> None:
        """Clean up after the email-analysis thread has finished."""
        if self.mail_worker is not None:
            self.mail_worker.deleteLater()
            self.mail_worker = None

        self.mailAnalysisChanged.emit(False)

    @Slot(list)
    def save_reviewed_mail_facts(self, facts: list[str]) -> None:
        """Save email facts selected and edited by the user.

        Args:
            facts: Reviewed factual passages selected for saving.
        """
        if not self.mail_review_pending:
            self.knowledgeSaveResult.emit(
                "Det finns inga mejlförslag att spara."
            )
            return

        if not facts or any(
            not isinstance(fact, str) or not fact.strip()
            for fact in facts
        ):
            self.knowledgeSaveResult.emit(
                "Välj minst en faktauppgift. Texten får inte vara tom."
            )
            return

        # Remove surrounding whitespace and exact duplicates.
        reviewed_facts = list(
            dict.fromkeys(fact.strip() for fact in facts)
        )

        added_count = 0

        try:
            for fact in reviewed_facts:
                embedding = create_embedding(fact)

                if add_knowledge(
                    fact,
                    embedding,
                    source=self.mail_review_source
                ):
                    added_count += 1

        except Exception as error:
            print(f"Saving email facts failed: {error}")
            self.knowledgeSaveResult.emit(
                f"Sparandet avbröts. {added_count} nya "
                "kunskapsposter hann sparas. Försök igen."
            )
            return

        self.discard_mail_review()

        self.knowledgeSaveResult.emit(
            f"Sparade {added_count} nya kunskapsposter. "
            "Eventuella dubbletter hoppades över."
        )


    @Slot()
    def discard_mail_review(self) -> None:
        """Clear the email suggestions without saving them."""
        self.mail_review_text = ""
        self.mail_review_facts = []
        self.mail_review_source = ""
        self.mail_review_pending = False

        self.mailReviewFinished.emit()

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


    @Slot(str, str, bool, bool, bool, bool, bool)
    def load_filtered_knowledge(
        self,
        search: str, 
        sort_order: str, 
        txt_active: bool, 
        docx_active: bool, 
        pdf_active: bool, 
        manual_active: bool,
        mail_active: bool
    ) -> None:
        """Load and filter knowledge for display in QML.
        
        Args:
            search: Search text matched against stored knowledge (text and source).
            sort_order: Sort order by creation time.
            txt_active: Whether TXT entries should be included or not.
            docx_active. Whether DOCX entries should be included or not.
            pdf_active: Whether PDF entries should be included or not.
            manual_active: whether manual entries should be included or not.
            mail_active: Whether EML and MSG entries should be included.
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
            elif mail_active and source.endswith((".eml", ".msg")):
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

        if item is None:
            print(f"Knowledge entry not found: {knowledge_id}")
            self.knowledgeSaveResult.emit(
                "Kunskapsposten kunde inte hittas."
            )
            return

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


    @Slot(str)
    def import_knowledge(self, file_path: str) -> None:
        """Import all knowledge entries from a JSON backup file.
        
            Args:
                file_path: Destination file URL received from QML.
        """

        local_path = QUrl(file_path).toLocalFile()

        try:
            imported_count, skipped_count = import_knowledge_from_json_file(
                local_path
            )

        except (FileNotFoundError, ValueError) as error:
            self.importResult.emit(str(error))
            return

        self.importResult.emit(
            f"Importerade {imported_count} poster. "
            f"Hoppade över {skipped_count} poster."
        )