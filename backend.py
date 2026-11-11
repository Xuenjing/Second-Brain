"""
Backend layer for the Second Brain application.

This module handles communication between QML and Python, manages
knowledge-base operations, and coordinates language-model generation
in a background thread.
"""

import sqlite3
from datetime import datetime
from pathlib import Path

from PySide6.QtCore import QObject, Signal, Slot, QUrl, QThread, QSettings

from retrieval import (
    retrieve_knowledge,
    create_embedding,
    get_embedding_model
)
from llm.local_provider import LocalLLMProvider
from database import (
    get_knowledge_sources,
    get_all_knowledge,
    get_knowledge_by_id,
    add_knowledge, 
    search_knowledge, 
    edit_knowledge,
    delete_knowledge_by_source, 
    delete_knowledge, 
    initialize_database
)
from imports.document_importer import import_docx_to_database
from imports.pdf_importer import import_pdf_to_database
from imports.text_importer import import_txt_to_database, read_txt_for_preview
from imports.mail_importer import import_mail_to_database
from imports.mail_parser import extract_mail_chunks
from imports.mail_fact_extractor import extract_mail_facts
from exporter import export_knowledge_to_json
from json_importer import import_knowledge_from_json_file
from imports.document_fact_extractor import extract_document_facts
from translator import translate



class Thinker(QThread):
    """Process a question without blocking the interface."""

    answerReady = Signal(str, list, list, list)
    answerFailed = Signal(str)

    def __init__(
        self, 
        llm: LocalLLMProvider, 
        question: str,
        top_k: int,
        similarity_threshold: float,
    ) -> None:
        """Initialize a background question-processing thread.

        Args:
            llm: Language-model provider used to generate the answer.
            question: User question.
        """
        super().__init__()
        self.llm = llm
        self.question = question
        self.top_k = top_k
        self.similarity_threshold = similarity_threshold

    def run(self) -> None:
        """Retrieve relevant knowledge and generate an answer."""

        try:
            results = retrieve_knowledge(
                self.question,
                top_k=self.top_k,
                similarity_threshold=self.similarity_threshold 
            )

            used_sources = results["used_sources"]
            additional_sources = results["additional_sources"]
            less_relevant_sources = results["less_relevant_sources"]

            if not used_sources:
                self.answerReady.emit(
                    "backend.answer.not_enough_info",
                    [],
                    additional_sources,
                    less_relevant_sources
                )
                return

            context = "\n".join(
                result["text"] for result in used_sources
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
            self.answerReady.emit(answer, used_sources, additional_sources, less_relevant_sources)

        except Exception as error:
            print(f"Answer generation failed: {error}")
            self.answerFailed.emit(
                "backend.answer.failed"
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
                "backend.model.load_failed"
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
                "backend.mail.analysis_failed"
            )

class DocumentFactWorker(QThread):
    """Suggest document facts without blocking the interface."""

    reviewReady = Signal(str, list, str)
    extractionFailed = Signal(str)

    def __init__(
        self,
        llm: LocalLLMProvider,
        document_text: str,
        source: str,
    ) -> None:
        """Keep the loaded model and a snapshot of the reviewed text."""
        super().__init__()
        self.llm = llm
        self.document_text = document_text
        self.source = source

    def run(self) -> None:
        """Analyze the document without saving any knowledge."""
        try:
            facts = extract_document_facts(
                self.document_text,
                self.llm,
            )
        except Exception as error:
            print(f"Document fact extraction failed: {error}")
            self.extractionFailed.emit(
                "document_analysis.failed"
            )
            return

        self.reviewReady.emit(
            self.document_text,
            facts,
            self.source,
        )

class Backend(QObject):
    """Handle communication between QML and application."""

    def __init__(self) -> None:
        """Initialize the database, backend and local language model."""
        super().__init__()

        # Keep the source of the document currently being reviewed.
        self.document_preview_source: str = ""

        # Keep the document-analysis thread alive until it finishes.
        self.document_worker: DocumentFactWorker | None = None

        # Retain suggestions until the user saves or discards them.
        self.document_review_text: str = ""
        self.document_review_facts: list[str] = []
        self.document_review_source: str = ""
        self.document_review_pending: bool = False

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

        self.settings = QSettings(
            "SecondBrain",
            "SecondBrain",
        )

        self.rag_top_k = self.settings.value(
            "rag/top_k",
            5,
            type=int,
        )

        self.rag_similarity_threshold = self.settings.value(
            "rag/similarity_threshold",
            0.82,
            type=float
        )

        initialize_database()

        # Preload embedding model during application startup.
        get_embedding_model()

        # lighter and faster model
        # self.llm = LocalLLMProvider("Qwen/Qwen3-0.6B")

        # medium model
        self.llm = LocalLLMProvider("Qwen/Qwen3-1.7B")
        
        # more demanding model
        # self.llm = LocalLLMProvider("Qwen/Qwen3-4B-Instruct-2507")


    def _language(self) -> str:
        """Return the currently selected interface language."""
        return self.settings.value(
            "ui/language",
            "sv",
            type=str,
        )


    def _text(self, key:str) -> str:
        """Return translated text for the current interface language."""
        return translate(
            key,
            self._language(),
        )

    # Signal from Python to QML with the text to display.
    replyReady = Signal(str, list, list, list)

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

    # Send the rag settings to QML.
    ragSettingsResult = Signal(bool, str)

    # Show settings for top_k and similarity_threshold.
    ragSettingsLoaded = Signal(int, float)

    # Send list of sources to QML.
    knowledgeSourcesLoaded = Signal(list)

    # Send number of entries deleted.
    knowledgeSourceDeleteResult = Signal(bool, str)  

    # Send document text and its source filename for review.
    documentPreviewReady = Signal(str, str)

    # Send a translation key when document preview fails.
    documentPreviewFailed = Signal(str)  

    # Report whether reviewed document text was saved.
    documentSaveResult = Signal(bool, str)

    # Notify QML when document analysis starts or finishes.
    documentAnalysisChanged = Signal(bool)

    # Send document text, suggested facts and source for review.
    documentReviewReady = Signal(str, list, str)

    # Report analysis errors using translation keys.
    documentAnalysisFailed = Signal(str)

    # Notify QML when document review has ended.
    documentReviewFinished = Signal()

    documentFactsSaveResult = Signal(bool, str, int)


    @Slot(int)
    def load_model(self, model_index: str) -> None:
        """Load the language model selected from the interface.
        
            Args:
                model_index: Name of the model that will be loaded.
        """
        if (self.thinker is not None or self.mail_worker is not None or self.document_worker is not None):
            self.modelLoadStatus.emit(
                self._text("backend.model.busy")
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
        self.modelLoadStatus.emit(
            self._text("backend.model.loading").format(
                model=model_name
            )
        )

        self.model_loader.start()


    @Slot(object)
    def handle_model_loaded(self, llm: LocalLLMProvider) -> None:
        """Replace the current language model after successful loading."""

        self.llm = llm
        self.modelLoadStatus.emit(
            self._text("backend.model.loaded").format(
                model=self.llm.model_name
            )
        )
        print(f"Model loaded {self.llm.model_name}")

    @Slot(str)
    def handle_model_load_error(self, message_key: str) -> None:
        """Handle errors that occur while loading a language model."""

        message = self._text(message_key)

        self.modelLoadStatus.emit(message)
        print(message)

    @Slot()
    def finish_model_loading(self) -> None:
        """Clean up after model loading has finished."""

        self.model_loader.deleteLater()
        self.model_loader = None

        self.modelLoadingChanged.emit(False)


    @Slot()
    def get_rag_settings(self) -> None:
        """Send the current RAG settings to QML."""

        self.ragSettingsLoaded.emit(
            self.rag_top_k,
            self.rag_similarity_threshold
        )


    @Slot(int, float)
    def set_rag_settings(
        self,
        top_k: int,
        similarity_threshold: float,
    ) -> None:
        """Validate and update the current rag retrieval settings."""

        if top_k < 1:
            self.ragSettingsResult.emit(
                False,
                self._text("backend.rag.top_k_min")
            )
            return
        if not 0.0 <= similarity_threshold <= 1.0:
            self.ragSettingsResult.emit(
                False,
                self._text("backend.rag.threshold_range")
            )
            return

     

        self.rag_top_k = top_k
        self.rag_similarity_threshold = similarity_threshold

        self.settings.setValue(
            "rag/top_k",
            top_k,
        )

        self.settings.setValue(
            "rag/similarity_threshold",
            similarity_threshold,
        )

        self.ragSettingsResult.emit(
            True,
            self._text("backend.rag.updated")
        )
        

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

        if (self.mail_worker is not None or self.model_loader is not None or self.document_worker is not None):
            self.replyFailed.emit(
                self._text("backend.reply.busy")
            )
            return

        self.thinker = Thinker(
            self.llm, 
            text,
            self.rag_top_k,
            self.rag_similarity_threshold,
        )

        # Receive the answer, errors and notification that the thread ended.
        self.thinker.answerReady.connect(self.handle_answer)
        self.thinker.answerFailed.connect(self.handle_error)
        self.thinker.finished.connect(self.finish_thinking)

        # Show the thinking indicator and start the background work.
        self.thinkingChanged.emit(True)
        self.thinker.start()

    @Slot(str, list, list, list)
    def handle_answer(
        self, 
        answer: str,
        used_sources: list,
        additional_sources: list, 
        less_relevant_sources: list,
    ) -> None:
        """Send the answer to QML.
        
        Args:
            answer: generated answer to display in QML interface.
        """
    def handle_answer(
        self,
        answer: str,
        used_sources: list,
        additional_sources: list,
        less_relevant_sources: list,
    ) -> None:
        """Send the answer to QML."""

        if not used_sources and answer == "backend.answer.not_enough_info":
            answer = self._text(answer)

        self.replyReady.emit(
            answer,
            used_sources,
            additional_sources,
            less_relevant_sources
        )

    @Slot(str)
    def handle_error(self, message_key: str) -> None:
        """Send the error message to QML.
        
        Args:
            message: error message to display in QML interface.
        """
        self.replyFailed.emit(
            self._text(message_key)
        )

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
                False,
                self._text("backend.knowledge.empty_text")
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
                False,
                self._text("backend.knowledge.duplicate")
            )
            return

        if updated:
            self.knowledgeEditResult.emit(
                True,
                self._text("backend.knowledge.updated")
            )
        else:
            self.knowledgeEditResult.emit(
                False,
                self._text("backend.knowledge.not_found")
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
                True,
                self._text("backend.knowledge.deleted")
            )
        else:
            self.knowledgeDeleteResult.emit(
                False,
                self._text("backend.knowledge.not_found")
            )


    @Slot(str)
    def delete_knowledge_source(self, source: str) -> None:
        """Delete all knowledge entries belonging to one source."""

        deleted_count = delete_knowledge_by_source(source)

        if deleted_count == 0:
            self.knowledgeSourceDeleteResult.emit(
                False,
                self._text("backend.source_delete.none")
            )
            return

        self.knowledgeSourceDeleteResult.emit(
            True,
            self._text(
                "backend.source_delete.success"
            ).format(
                count=deleted_count
            )
        )
            
    
    @Slot(str)
    def add_manual_knowledge(self, text: str) -> None:
        """
        Add manually added text to knowledge database.

        Args:
            text: knowledge text received from QML.
        """

        if not text.strip():
            self.knowledgeSaveResult.emit(
                self._text("backend.manual.empty")
            )
            return

        embedding = create_embedding(text)

        added = add_knowledge(
            text, 
            embedding,
            source="manual"
        )

        if added:
            self.knowledgeSaveResult.emit(
                self._text("backend.manual.added")
            )
        else:
            self.knowledgeSaveResult.emit(
                self._text("backend.manual.no_new")
            )

    @Slot(str)
    def import_dropped_document(self, file_url: str) -> None:
        """Validate a dropped document and use its existing importer."""
        url = QUrl(file_url)

        if not url.isLocalFile():
            self.knowledgeSaveResult.emit(
                self._text("backend.drop.local_only")
            )
            return

        path = Path(url.toLocalFile())

        if not path.is_file():
            self.knowledgeSaveResult.emit(
                self._text("backend.drop.not_found")
            )
            return

        importers = {
            ".txt": self.preview_txt,
            ".pdf": self.add_pdf_knowledge,
            ".docx": self.add_docx_knowledge,
            ".eml": self.preview_mail,
            ".msg": self.preview_mail,
        }

        importer = importers.get(path.suffix.lower())

        if importer is None:
            self.knowledgeSaveResult.emit(
                self._text("backend.drop.unsupported")
            )
            return

        importer(file_url)

    @Slot(str)
    def preview_txt(self, file_url: str) -> None:
        """Read a TXT file for preview without saving knowledge.

        Args:
            file_url: Local file URL received from QML.
        """

        if self.document_worker is not None:
            self.documentPreviewFailed.emit(
                "document_analysis.busy"
            )
            return

        if self.document_review_pending:
            self.documentPreviewFailed.emit(
                "document_analysis.review_pending"
            )
            return

        url = QUrl(file_url)

        if not url.isLocalFile():
            self.documentPreviewFailed.emit(
                "document_import.read_failed"
            )
            return

        path = Path(url.toLocalFile())

        if path.suffix.lower() != ".txt":
            self.documentPreviewFailed.emit(
                "document_import.read_failed"
            )
            return

        try:
            text = read_txt_for_preview(str(path))
        except ValueError as error:
            self.documentPreviewFailed.emit(str(error))
            return
        except OSError as error:
            print(f"Reading TXT preview failed: {error}")
            self.documentPreviewFailed.emit(
                "document_import.read_failed"
            )
            return

        self.document_preview_source = path.name
        self.documentPreviewReady.emit(text, path.name)

    @Slot(str, str)
    def analyze_previewed_document(
        self,
        text: str,
        source: str,
    ) -> None:
        """Analyze reviewed document text using the loaded model."""
        if (
            not self.document_preview_source
            or source != self.document_preview_source
        ):
            self.documentAnalysisFailed.emit(
                "document_import.read_failed"
            )
            return

        if not text.strip():
            self.documentAnalysisFailed.emit(
                "document_save.empty_text"
            )
            return

        if (
            self.thinker is not None
            or self.model_loader is not None
            or self.mail_worker is not None
            or self.document_worker is not None
        ):
            self.documentAnalysisFailed.emit(
                "document_analysis.busy"
            )
            return

        if self.document_review_pending:
            self.documentAnalysisFailed.emit(
                "document_analysis.review_pending"
            )
            return

        self.document_worker = DocumentFactWorker(
            self.llm,
            text,
            source,
        )

        self.document_worker.reviewReady.connect(
            self.handle_document_review
        )
        self.document_worker.extractionFailed.connect(
            self.handle_document_analysis_error
        )
        self.document_worker.finished.connect(
            self.finish_document_analysis
        )

        self.documentAnalysisChanged.emit(True)
        self.document_worker.start()

    @Slot(str, list, str)
    def handle_document_review(
        self,
        text: str,
        facts: list[str],
        source: str,
    ) -> None:
        """Retain suggestions for manual review without saving them."""
        self.document_review_text = text
        self.document_review_facts = facts
        self.document_review_source = source
        self.document_review_pending = True

        self.documentReviewReady.emit(text, facts, source)

    @Slot(str)
    def handle_document_analysis_error(self, message_key: str) -> None:
        """Forward a translated-error key to the interface."""
        self.documentAnalysisFailed.emit(message_key)

    @Slot()
    def finish_document_analysis(self) -> None:
        """Release the worker after its thread has finished."""
        if self.document_worker is not None:
            self.document_worker.deleteLater()
            self.document_worker = None

        self.documentAnalysisChanged.emit(False)

    @Slot(list)
    def save_reviewed_document_facts(self, facts: list[str]) -> None:
        """Save only the document facts selected and edited by the user."""
        if self.document_worker is not None:
            self.documentFactsSaveResult.emit(
                False,
                "document_analysis.busy",
                0,
            )
            return

        if not self.document_review_pending:
            self.documentFactsSaveResult.emit(
                False,
                "document_review.no_pending",
                0,
            )
            return

        if not facts or any(
            not isinstance(fact, str) or not fact.strip()
            for fact in facts
        ):
            self.documentFactsSaveResult.emit(
                False,
                "document_review.invalid_selection",
                0,
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
                    source=self.document_review_source,
                ):
                    added_count += 1
        except Exception as error:
            print(f"Saving document facts failed: {error}")
            self.documentFactsSaveResult.emit(
                False,
                "document_review.save_failed",
                added_count,
            )
            return

        self.discard_document_review()

        self.documentFactsSaveResult.emit(
            True,
            "document_review.saved",
            added_count,
        )

    @Slot()
    def discard_document_review(self) -> None:
        """Clear document suggestions without saving them."""
        if self.document_worker is not None:
            self.documentAnalysisFailed.emit(
                "document_analysis.busy"
            )
            return

        self.document_review_text = ""
        self.document_review_facts = []
        self.document_review_source = ""
        self.document_review_pending = False

        self.documentReviewFinished.emit()

    @Slot(str, str)
    def save_previewed_document(self, text: str, source: str) -> None:
        """Save document text reviewed and edited by the user.

        Args:
            text: Current text from the preview dialog.
            source: Filename associated with the preview.
        """

        if self.document_worker is not None:
            self.documentSaveResult.emit(
                False,
                "document_analysis.busy"
            )
            return

        if self.document_review_pending:
            self.documentSaveResult.emit(
                False,
                "document_analysis.review_pending"
            )
            return

        if (
            not self.document_preview_source
            or source != self.document_preview_source
        ):
            self.documentSaveResult.emit(
                False,
                "document_import.read_failed"
            )
            return

        reviewed_text = text.strip()

        if not reviewed_text:
            self.documentSaveResult.emit(
                False,
                "document_save.empty_text"
            )
            return

        try:
            embedding = create_embedding(reviewed_text)

            added = add_knowledge(
                reviewed_text,
                embedding,
                source=self.document_preview_source
            )
        except Exception as error:
            print(f"Saving reviewed document failed: {error}")
            self.documentSaveResult.emit(
                False,
                "document_save.failed"
            )
            return

        self.documentSaveResult.emit(
            True,
            "document_save.saved"
            if added
            else "document_save.already_exists"
        )

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
            self.knowledgeSaveResult.emit(
                self._text("backend.import.file_missing")
            )
            return
        except ValueError as error:
            self.knowledgeSaveResult.emit(str(error))
            return
        
        if added_count == 0:
            self.knowledgeSaveResult.emit(
                self._text("backend.import.none_added")
            )
        else:
            self.knowledgeSaveResult.emit(
                self._text(
                    "backend.import.txt_success"
                ).format(
                    count=added_count
                )
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
            self.knowledgeSaveResult.emit(
                self._text("backend.import.none_added")
            )
        else:
            self.knowledgeSaveResult.emit(
                self._text(
                    "backend.import.docx_success"
                ).format(
                    count=added_count
                )
            )


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
            self.knowledgeSaveResult.emit(
                self._text("backend.import.none_added")
            )
        else:
            self.knowledgeSaveResult.emit(
                self._text(
                    "backend.import.pdf_success"
                ).format(
                    count=added_count
                )
            )

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

    @Slot(str)
    def save_previewed_mail(self, email_text: str) -> None:
        """Save the email text reviewed and edited by the user.

        Args:
            email_text: Current email text received from QML.
        """
        if not email_text.strip():
            self.knowledgeSaveResult.emit(
                self._text("backend.mail.empty_save")
            )
            return

        try:
            embedding = create_embedding(email_text)

            added = add_knowledge(
                email_text,
                embedding,
                source=self.mail_source
            )
        except Exception as error:
            print(f"Saving email failed: {error}")
            self.knowledgeSaveResult.emit(
                self._text("backend.mail.save_failed")
            )
            return

        if added:
            self.knowledgeSaveResult.emit(
                self._text("backend.mail.saved")
            )
        else:
            self.knowledgeSaveResult.emit(
                self._text("backend.mail.duplicate")
            )

    @Slot(str)
    def analyze_previewed_mail(self, email_text: str) -> None:
        """Analyze the email text reviewed and edited by the user.

        Args:
            email_text: Current email text received from QML.
        """
        if not email_text.strip():
            self.knowledgeSaveResult.emit(
                self._text("backend.mail.empty_analysis")
            )
            return

        if (
            self.thinker is not None
            or self.model_loader is not None
            or self.mail_worker is not None
            or self.document_worker is not None
        ):
            self.knowledgeSaveResult.emit(
                self._text("backend.mail.busy")
            )
            return

        if self.mail_review_pending:
            self.knowledgeSaveResult.emit(
                self._text("backend.mail.review_pending")
            )
            return

        self.mail_worker = MailFactWorker(
            self.llm,
            email_text,
            self.mail_source
        )

        self.mail_worker.reviewReady.connect(self.handle_mail_review)
        self.mail_worker.extractionFailed.connect(self.handle_mail_error)
        self.mail_worker.finished.connect(self.finish_mail_analysis)

        self.knowledgeSaveResult.emit(
            self._text("backend.mail.analyzing")
        )
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
            self._text("backend.mail.analysis_ready")
        )

        self.mailReviewReady.emit(email_text, facts, source)

    @Slot()
    def reopen_mail_review(self) -> None:
        """Send pending email suggestions to the interface again."""
        if not self.mail_review_pending:
            self.knowledgeSaveResult.emit(
                self._text("backend.mail.no_review")
            )
            return

        self.mailReviewReady.emit(
            self.mail_review_text,
            self.mail_review_facts,
            self.mail_review_source
        )

    @Slot(str)
    def handle_mail_error(self, message_key: str) -> None:
        """Display an email-analysis error.

        Args:
            message_key: Error message to display.
        """
        self.knowledgeSaveResult.emit(
            self._text(message_key)
        )


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
                self._text("backend.mail.no_facts_to_save")
            )
            return

        if not facts or any(
            not isinstance(fact, str) or not fact.strip()
            for fact in facts
        ):
            self.knowledgeSaveResult.emit(
                self._text("backend.mail.invalid_selection")
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
                self._text(
                    "backend.mail.fact_save_failed"
                ).format(
                    count=added_count
                )
            )
            return

        self.discard_mail_review()

        self.knowledgeSaveResult.emit(
            self._text(
                "backend.mail.fact_save_success"
            ).format(
                count=added_count
            )
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
                self._text("backend.mail.file_missing")
            )
            return
        except ValueError as error:
            self.knowledgeSaveResult.emit(str(error))
            return
        except OSError:
            self.knowledgeSaveResult.emit(
                self._text("backend.mail.read_failed")
            )
            return

        if added_count == 0:
            self.knowledgeSaveResult.emit(
                self._text("backend.mail.none_added")
            )
        else:
            self.knowledgeSaveResult.emit(
                self._text(
                    "backend.mail.import_success"
                ).format(
                    count=added_count
                )
            )


    @Slot(str, str, bool, bool, bool, bool, bool, str)
    def load_filtered_knowledge(
        self,
        search: str, 
        sort_order: str, 
        txt_active: bool, 
        docx_active: bool, 
        pdf_active: bool, 
        manual_active: bool,
        mail_active: bool,
        selected_source: str,
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

            # If a specific source is chosen, skip every post not from that source.
            if selected_source:
                if item["source"] != selected_source:
                    continue

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


    @Slot(str, bool, bool, bool, bool, bool)
    def load_filtered_sources(
        self,
        sort_order: str,
        txt_active: bool,
        docx_active: bool,
        pdf_active: bool,
        manual_active: bool,
        mail_active: bool,
    ) -> None:
        """Load and filter group knowledge sources for display in QML."""

        sources = get_knowledge_sources(sort_order)

        filtered_sources = []

        for item in sources:
            source = item["source"].lower()

            if txt_active and source.endswith(".txt"):
                filtered_sources.append(item)
            elif docx_active and source.endswith(".docx"):
                filtered_sources.append(item)
            elif pdf_active and source.endswith(".pdf"):
                filtered_sources.append(item)
            elif manual_active and source == "manual":
                filtered_sources.append(item)
            elif mail_active and source.endswith((".eml", ".msg")):
                filtered_sources.append(item)

        for item in filtered_sources:
            source_date = datetime.fromisoformat(item["source_date"])

            item["source_date"] = source_date.strftime("%Y-%m-%d %H:%M")

        self.knowledgeSourcesLoaded.emit(filtered_sources)
            

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
                self._text("backend.knowledge.not_found")
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
            self.exportResult.emit(
                self._text("backend.backup.export_failed")
            )
            return

        self.exportResult.emit(
            self._text(
                "backend.backup.export_success"
            ).format(
                count=exported_count
            )
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
            self._text(
                "backend.backup.import_success"
            ).format(
                imported=imported_count,
                skipped=skipped_count,
            )
        )