"""
Provide translation support for the Second Brain application.

This module stores available translations and exposes a Translator class
that allows QML and Python code to access translated interface text and
switch between supported languages.
"""

from PySide6.QtCore import QObject, Property, Signal, Slot, QSettings


TRANSLATIONS = {
    "sv": {
        # Common
        "common.save": "Spara",
        "common.close": "Stäng",
        "common.reset": "Återställ",
        "common.cancel": "Avbryt",
        "common.delete": "Ta bort",

        # Settings
        "settings.title": "Inställningar",
        "settings.language": "Språk",

        # Appearance
        "settings.appearance": "Utseende",
        "settings.light": "Ljust",
        "settings.dark": "Mörkt",
        "settings.theme.accessible":
            "Byt mellan ljust och mörkt läge",
        "settings.theme.to_light":
            "Byt till ljust läge",
        "settings.theme.to_dark":
            "Byt till mörkt läge",

        # Backup
        "settings.backup": "Back-up",
        "settings.export_database": "Exportera databas",
        "settings.import_database": "Importera databas",

        # RAG
        "settings.rag": "RAG-inställningar",
        "settings.top_k": "Top-K",
        "settings.similarity_threshold": "Likhetströskel",
        "settings.save_rag": "Spara RAG-inställningar",
        "settings.reset_rag": "Återställ standardvärden",

        # Knowledge dialog
        "knowledge.add_title": "Lägg till kunskap",
        "knowledge.input_label": "Skriv eller klistra in information:",
        "knowledge.input_placeholder": "Information till kunskapsbasen",
        "knowledge.save": "Spara kunskap",
        "knowledge.import_txt": "Importera .txt-fil",
        "knowledge.import_docx": "Importera .docx-fil",
        "knowledge.import_pdf": "Importera .pdf-fil",
        "knowledge.input_label": "Skriv eller klistra in information",
        "knowledge.drop_files":
            "Dra hit en TXT-, PDF-, DOCX-, EML- eller MSG-fil",
        "knowledge.drop_here":
            "Släpp filen här",            
        "knowledge.import_mail":
            "Importera mejl (.eml eller .msg)",

        # File dialog
        "filedialog.select_txt": "Välj en textfil",
        "filedialog.txt_files": "Textfiler (*.txt)",

        "filedialog.select_docx": "Välj en DOCX-fil",
        "filedialog.docx_files": "Word-dokument (*.docx)",

        "filedialog.select_pdf": "Välj en PDF-fil",
        "filedialog.pdf_files": "PDF-dokument (*.pdf)",

        "filedialog.save_backup": "Spara säkerhetskopia",
        "filedialog.json_files": "JSON-filer (*.json)",    

        # Knowledge view
        "knowledge_view.title": "Kunskapsbas",
        "knowledge_view.search": "Sök bland sparad kunskap",
        "knowledge_view.show_posts": "Visa poster",
        "knowledge_view.show_sources": "Visa källor",
        "knowledge_view.posts_shown": "Visar {count} kunskapsposter",
        "knowledge_view.no_posts": "Inga kunskapsposter att visa.",   
        "knowledge_view.showing": "Visar",
        "knowledge_view.knowledge_entries": "kunskapsposter",    

        "knowledge_view.filter_txt": "TXT-filer",
        "knowledge_view.filter_docx": "DOCX-filer",
        "knowledge_view.filter_pdf": "PDF-filer",
        "knowledge_view.filter_mail": "Mejl",
        "knowledge_view.filter_manual": "Manuella poster",

        "knowledge_view.sort_oldest": "Äldst först",
        "knowledge_view.sort_newest": "Nyast först",

        "knowledge_view.source": "Källa:",
        "knowledge_view.created": "Skapad:",
        "knowledge_view.added": "Tillagd:",
        "knowledge_view.entries": "kunskapsposter",

        "knowledge_view.edit_post": "Redigera kunskapspost",
        "knowledge_view.delete_post": "Ta bort kunskapspost",

        "knowledge_view.view_source": "Visa poster från källan",
        "knowledge_view.delete_source": "Ta bort källa",   

        # Edit knowledge dialog.
        "edit_knowledge.title": "Redigera kunskap",
        "edit_knowledge.placeholder": "Ändra kunskapspostens text",
        "edit_knowledge.save_changes": "Spara ändringar",
        "edit_knowledge.close_without_saving": "Stäng utan att spara",

        # Delete knowledge dialog.
        "delete_knowledge.title": "Ta bort kunskap",
        "delete_knowledge.confirm": "Vill du ta bort den här kunskapsposten?",

        # Delete source dialog.
        "delete_source.title": "Ta bort källa",
        "delete_source.confirm": "Vill du ta bort alla kunskapsposter från den här källan?",
        "delete_source.entries": "Kunskapsposter:",
        "delete_source.all": "Ta bort alla",
        "delete_source.warning": "Detta går inte att ångra",

        # Source dialog.
        "source_dialog.title": "Källor",
        "source_dialog.search": "Sök bland källor",
        "source_dialog.showing": "Visar",
        "source_dialog.of": "av",
        "source_dialog.source_entry": "källpost",
        "source_dialog.source_entries": "källposter",
        "source_dialog.score": "Likhet",
        "source_dialog.no_search_results": "Inga källor matchar sökningen.",
        "source_dialog.show_used_only": "Visa endast använda källor",
        "source_dialog.show_more_relevant": "Visa fler relevanta källor",

        # Main toolbar.
        "toolbar.add_knowledge": "Lägg till kunskap",
        "toolbar.view_knowledge": "Visa kunskapsposter",

        "toolbar.model_fast": "Qwen3 0.6B — Snabb",
        "toolbar.model_recommended": "Qwen3 1.7B — Rekommenderas",
        "toolbar.model_slow": "Qwen3 4B — Långsam",

        "toolbar.load_model": "Ladda modell",
        "toolbar.loading_model": "Laddar...",

    },

    "en": {
        # Common
        "common.save": "Save",
        "common.close": "Close",
        "common.reset": "Reset",
        "common.cancel": "Cancel",
        "common.delete": "Delete",

        # Settings
        "settings.title": "Settings",
        "settings.language": "Language",

        # Appearance
        "settings.appearance": "Appearance",
        "settings.light": "Light",
        "settings.dark": "Dark",
        "settings.theme.accessible":
            "Switch between light and dark mode",
        "settings.theme.to_light":
            "Switch to light mode",
        "settings.theme.to_dark":
            "Switch to dark mode",

        # Backup
        "settings.backup": "Backup",
        "settings.export_database": "Export database",
        "settings.import_database": "Import database",

        # RAG
        "settings.rag": "RAG settings",
        "settings.top_k": "Top-K",
        "settings.similarity_threshold": "Similarity threshold",
        "settings.save_rag": "Save RAG settings",
        "settings.reset_rag": "Reset to defaults",

        # Knowledge dialog
        "knowledge.add_title": "Add knowledge",
        "knowledge.input_label": "Write or paste information:",
        "knowledge.input_placeholder": "Information for the knowledge base",
        "knowledge.save": "Save knowledge",
        "knowledge.import_txt": "Import .txt file",
        "knowledge.import_docx": "Import .docx file",
        "knowledge.import_pdf": "Import .pdf file",

        "knowledge.input_label": "Write or paste information",
        "knowledge.drop_files":
            "Drop a TXT, PDF, DOCX, EML, or MSG file here",
        "knowledge.drop_here":
            "Drop the file here",
        "knowledge.import_mail":
            "Import email (.eml or .msg)",   

        # File dialog
        "filedialog.select_txt": "Select a text file",
        "filedialog.txt_files": "Text files (*.txt)",

        "filedialog.select_docx": "Select a DOCX file",
        "filedialog.docx_files": "Word documents (*.docx)",

        "filedialog.select_pdf": "Select a PDF file",
        "filedialog.pdf_files": "PDF documents (*.pdf)",

        "filedialog.save_backup": "Save backup",
        "filedialog.json_files": "JSON files (*.json)",    

        # Knowledge view
        "knowledge_view.title": "Knowledge base",
        "knowledge_view.search": "Search saved knowledge",
        "knowledge_view.show_posts": "Show entries",
        "knowledge_view.show_sources": "Show sources",
        "knowledge_view.posts_shown": "Showing {count} knowledge entries",
        "knowledge_view.no_posts": "No knowledge entries to display.",
        "knowledge_view.showing": "Showing",
        "knowledge_view.knowledge_entries": "knowledge entries",

        "knowledge_view.filter_txt": "TXT files",
        "knowledge_view.filter_docx": "DOCX files",
        "knowledge_view.filter_pdf": "PDF files",
        "knowledge_view.filter_mail": "Email",
        "knowledge_view.filter_manual": "Manual entries",

        "knowledge_view.sort_oldest": "Oldest first",
        "knowledge_view.sort_newest": "Newest first", 

        "knowledge_view.source": "Source:",
        "knowledge_view.created": "Created:",
        "knowledge_view.added": "Added:",
        "knowledge_view.entries": "knowledge entries",

        "knowledge_view.edit_post": "Edit knowledge entry",
        "knowledge_view.delete_post": "Delete knowledge entry",

        "knowledge_view.view_source": "View entries from source",
        "knowledge_view.delete_source": "Delete source",      

        # Edit knowledge dialog.
        "edit_knowledge.title": "Edit knowledge",
        "edit_knowledge.placeholder": "Edit the knowledge entry text",
        "edit_knowledge.save_changes": "Save changes",
        "edit_knowledge.close_without_saving": "Close without saving",         

        # Delete knowledge dialog.
        "delete_knowledge.title": "Delete knowledge",
        "delete_knowledge.confirm": "Do you want to delete this knowledge entry?",

        # Delete source dialog.
        "delete_source.title": "Delete source",
        "delete_source.confirm": "Do you want to delete all knowledge entries from this source?",
        "delete_source.entries": "Knowledge entries:",
        "delete_source.all": "Delete all",
        "delete_source.warning": "This cannot be undone",

        # Source dialog.
        "source_dialog.title": "Sources",
        "source_dialog.search": "Search sources",
        "source_dialog.showing": "Showing",
        "source_dialog.of": "of",
        "source_dialog.source_entry": "source entry",
        "source_dialog.source_entries": "source entries",
        "source_dialog.score": "Similarity",
        "source_dialog.no_search_results": "No sources match the search.",
        "source_dialog.show_used_only": "Show used sources only",
        "source_dialog.show_more_relevant": "Show more relevant sources",   

        # Main toolbar.
        "toolbar.add_knowledge": "Add knowledge",
        "toolbar.view_knowledge": "View knowledge entries",
        "toolbar.model_fast": "Qwen3 0.6B — Fast",
        "toolbar.model_recommended": "Qwen3 1.7B — Recommended",
        "toolbar.model_slow": "Qwen3 4B — Slow",
        "toolbar.load_model": "Load model",
        "toolbar.loading_model": "Loading...",

    },
}


class Translator(QObject):
    languageChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.settings = QSettings("SecondBrain", "SecondBrain")


        self._language = self.settings.value(
            "ui/language",
            "sv",
            type=str
        )

    # Decorating function with property to make it easier for QML to call for it.
    @Property(str, notify=languageChanged)
    def language(self):
        return self._language

    @Slot(str)
    def set_language(self, language: str):
        if language not in TRANSLATIONS:
            return
        if language == self._language:
            return

        self._language = language

        self.settings.setValue(
            "ui/language",
            language
        )

        self.languageChanged.emit()

    @Slot(str, str, result=str)
    def text(self, key:str, language:str) -> str:
        return TRANSLATIONS.get(
            language,
            TRANSLATIONS["sv"]
        ).get(key, key)

    
