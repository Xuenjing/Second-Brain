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

    },

    "en": {
        # Common
        "common.save": "Save",
        "common.close": "Close",
        "common.reset": "Reset",
        "common.cancel": "Cancel",

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

    
