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

        # RAG
        "settings.rag": "RAG-inställningar",
        "settings.top_k": "Top-K",
        "settings.similarity_threshold": "Likhetströskel",
        "settings.save_rag": "Spara RAG-inställningar",
        "settings.reset_rag": "Återställ standardvärden",
    },

    "en": {
        # Common
        "common.save": "Save",
        "common.close": "Close",
        "common.reset": "Reset",

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

        # RAG
        "settings.rag": "RAG settings",
        "settings.top_k": "Top-K",
        "settings.similarity_threshold": "Similarity threshold",
        "settings.save_rag": "Save RAG settings",
        "settings.reset_rag": "Reset to defaults",
    },
}


class Translator(QObject):
    languageChanged = Signal()

    def __init__(self):
        super().__init__()

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

    
