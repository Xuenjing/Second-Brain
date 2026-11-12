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
        "settings.invalid_threshold": (
            "Likhetströskeln måste vara ett giltigt tal mellan 0 och 1."
        ),

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

        # Header
        "header.user_guide": "Användarguide",

        # Thinking
        "thinking.status": "Tänker…",

        # Chatinput.
        "chat_input.placeholder": "Skriv din fråga här",
        "chat_input.send": "Skicka",

        # Chatview.
        "chat_view.welcome": "Vad vill du veta?",

        # Chat message.
        "chat_message.you": "Du",
        "chat_message.review_facts": "Granska föreslagna fakta",
        "chat_message.source": "källa",
        "chat_message.sources": "källor",
        "chat_message.entry": "post",
        "chat_message.entries": "poster",
        "chat_message.click_for_details": "Klicka för detaljer",

        # Model load.
        "model_load.title": "Byta språkmodell?",
        "model_load.warning": (
            "Att ladda en ny modell kan ta från några sekunder till flera minuter "
            "beroende på modellstorlek, hårdvara och om modellen redan finns lokalt. "
            "Om modellen saknas kan den behöva laddas ner först."
        ),
        "model_load.confirm": "Ladda modell",

        # Mail review.
        "mail_review.title_prefix": "Granska fakta:",
        "mail_review.close": "Stäng granskningen",
        "mail_review.close_keep": "Stäng och behåll förslagen",
        "mail_review.discard": "Kasta förslagen",
        "mail_review.save_selected": "Spara valda fakta",
        "mail_review.empty_selected_error":
            "Valda faktauppgifter får inte vara tomma.",
        "mail_review.none_selected_error":
            "Välj minst en faktauppgift att spara.",
        "mail_review.original_email": "Originalmejl",
        "mail_review.select_edit": "Välj och redigera fakta",
        "mail_review.check_warning":
            "Kontrollera förslagen mot originalet. "
            "AI:n kan missa eller misstolka information.",
        "mail_review.no_facts":
            "AI:n föreslog inga faktauppgifter.",
        "mail_review.include_suggestion":
            "Ta med förslag",

        # Mail preview.
        "mail_preview.title": "Förhandsgranska mejl",
        "mail_preview.save_full": "Spara hela mejlet",
        "mail_preview.review_suggestions": "Granska förslag",
        "mail_preview.suggest_facts": "Föreslå fakta med AI",
        "mail_preview.preview_prefix": "Förhandsgranska:",
        "mail_preview.close_preview": "Stäng förhandsgranskningen",

        # Mail analysis
        "mail_analysis.title": "Analysera mejl med AI?",
        "mail_analysis.warning": (
            "AI-analysen kan ta flera minuter beroende på mejlets längd, "
            "den laddade modellen och datorns prestanda. Du får granska och "
            "redigera förslagen innan något sparas."
        ),
        "mail_analysis.analyze": "Analysera mejl",

        # Main QML.
        "filedialog.select_mail": "Välj ett mejl",
        "filedialog.mail_files": "Mejlfiler (*.eml *.msg)",
        "filedialog.import_backup": "Importera backup",
        "status.exporting": "Exporterar…",
        "status.error_prefix": "Fel:",
        "mail_status.analyzing": "Analyserar mejl…",
        "mail_status.analysis_failed":
            "Mejlet kunde inte analyseras. Försök igen.",
        "mail_status.analysis_done": "Mejlanalysen är klar.",
        "mail_status.suggestions_to_review": "förslag att granska.",
        "mail_status.no_facts":
            "Inga faktauppgifter föreslogs.",
        "mail_status.review_finished":
            "Mejlgranskningen är avslutad.",
        "mail_status.analysis_of": "Analysen av mejlet",
        "mail_status.is_done": "är klar.",

        # Document preview.
        "document_preview.title": "Granska dokument",
        "document_preview.edit_hint":
            "Granska och redigera texten före sparande.",

        # Document import errors.
        "document_import.invalid_encoding":
            "Textfilen kunde inte läsas. Spara den som UTF-8 och försök igen.",
        "document_import.empty_file":
            "Textfilen är tom.",
        "document_import.read_failed":
            "Filen kunde inte läsas. Kontrollera att den finns och går att öppna.",

        # Document saving.
        "document_save.empty_text": "Det finns ingen text att spara.",
        "document_save.saved": "Dokumenttexten har sparats.",
        "document_save.already_exists":
            "Texten finns redan i kunskapsbasen.",
        "document_save.failed":
            "Dokumenttexten kunde inte sparas. Försök igen.",
        "document_save.save_full": "Spara som en post",
        "document_save.single_tooltip":
            "Spara hela texten som en kunskapspost",
        "document_save.save_chunks": "Spara uppdelat",
        "document_save.chunks_tooltip":
            "Spara varje stycke som en egen post",
        "document_save.chunks_saved": (
            "Sparade {count} nya kunskapsposter. "
            "Eventuella dubbletter hoppades över."
        ),
        "document_save.chunks_failed": (
            "Sparandet avbröts. {count} nya kunskapsposter hann sparas. "
            "Texten finns kvar. Försök igen."
        ),
        "document_analysis.failed":
        "Dokumentet kunde inte analyseras. Försök igen.",
        "document_analysis.busy":
            "Vänta tills det pågående arbetet är klart.",
        "document_analysis.review_pending":
            "Granska och spara eller kasta dokumentförslagen först.",
        "document_analysis.title": "Analysera dokument med AI?",
        "document_analysis.warning": (
            "AI-analysen kan ta flera minuter beroende på textens längd, "
            "den laddade modellen och datorns prestanda. Du får granska "
            "och redigera förslagen innan något sparas."
        ),
        "document_analysis.analyze": "Analysera dokument",
        "document_preview.suggest_facts": "Föreslå fakta med AI",
        
        # Document review.
        "document_review.original_text": "Text som analyserades",
        "document_review.check_warning": (
            "Kontrollera förslagen mot dokumenttexten. "
            "AI:n kan missa eller misstolka information."
        ),

        "document_review.no_pending":
            "Det finns inga dokumentförslag att spara.",
        "document_review.invalid_selection":
            "Välj minst en faktauppgift. Valda texter får inte vara tomma.",
        "document_review.saved": (
            "Sparade {count} nya kunskapsposter. "
            "Eventuella dubbletter hoppades över."
        ),
        "document_review.save_failed": (
            "Sparandet avbröts. {count} nya kunskapsposter hann sparas. "
            "Granskningen finns kvar. Försök igen."
        ),

        "document_analysis.analyzing": "Analyserar dokument…",
        "document_analysis.ready":
            "Analysen är klar. Granska förslagen innan du sparar.",
        "document_analysis.no_facts":
            "Analysen är klar. Inga faktauppgifter föreslogs.",        
        "document_review.finished": "Dokumentgranskningen är avslutad.",

        # Backend - model
        "backend.model.busy":
            "Vänta tills det pågående arbetet är klart.",
        "backend.model.loading":
            "Laddar modell: {model}",
        "backend.model.loaded":
            "Modellen har laddats: {model}",

        # Backend - RAG
        "backend.rag.top_k_min":
            "Top-K måste vara minst 1.",
        "backend.rag.threshold_range":
            "Likhetströskeln måste vara mellan 0.0 och 1.0.",
        "backend.rag.updated":
            "RAG-inställningarna har uppdaterats.",

        # Backend - question processing
        "backend.reply.busy":
            "Modellen är upptagen. Vänta tills arbetet är klart.",

        # Backend - knowledge editing
        "backend.knowledge.empty_text":
            "Texten får inte vara tom.",
        "backend.knowledge.duplicate":
            "Det finns redan en post med samma text.",
        "backend.knowledge.updated":
            "Kunskapsposten har uppdaterats.",
        "backend.knowledge.not_found":
            "Kunskapsposten kunde inte hittas.",
        "backend.knowledge.deleted":
            "Kunskapsposten har tagits bort.",

        # Backend - source deletion
        "backend.source_delete.none":
            "Inga kunskapsposter kunde tas bort.",
        "backend.source_delete.success":
            "{count} kunskapsposter togs bort.",

        # Backend - manual knowledge
        "backend.manual.empty":
            "Ingen kunskap lades till.",
        "backend.manual.added":
            "Kunskap har lagts till.",
        "backend.manual.no_new":
            "Ingen ny kunskap lades till.",

        # Backend - dropped documents
        "backend.drop.local_only":
            "Släpp en lokal fil från datorn.",
        "backend.drop.not_found":
            "Filen kunde inte hittas. Mappar kan inte importeras.",
        "backend.drop.unsupported":
            "Filtypen stöds inte. Välj TXT, PDF, DOCX, EML eller MSG.",

        # Backend - document import
        "backend.import.file_missing":
            "Den valda filen finns inte.",
        "backend.import.none_added":
            "Ingen ny kunskap lades till.",

        "backend.import.txt_success":
            "Importerade {count} kunskapsposter från textfil.",
        "backend.import.docx_success":
            "Importerade {count} kunskapsposter från DOCX-fil.",
        "backend.import.pdf_success":
            "Importerade {count} kunskapsposter från PDF-fil.",

        # Backend - mail
        "backend.mail.empty_save":
            "Det finns inget mejl att spara.",
        "backend.mail.save_failed":
            "Mejlet kunde inte sparas. Försök igen.",
        "backend.mail.saved":
            "Mejlet har sparats.",
        "backend.mail.duplicate":
            "Mejlet finns redan i kunskapsbasen.",

        "backend.mail.empty_analysis":
            "Det finns inget mejl att analysera.",
        "backend.mail.busy":
            "Vänta tills det pågående arbetet är klart.",
        "backend.mail.review_pending":
            "Granska eller kasta de tidigare förslagen först.",
        "backend.mail.analyzing":
            "Analyserar mejlet…",
        "backend.mail.analysis_ready":
            "Mejlanalysen är klar. Granska förslagen innan du sparar.",
        "backend.mail.analysis_failed":
            "Mejlet kunde inte analyseras. Försök igen.",

        "backend.mail.no_review":
            "Det finns inga mejlförslag att granska.",
        "backend.mail.no_facts_to_save":
            "Det finns inga mejlförslag att spara.",
        "backend.mail.invalid_selection":
            "Välj minst en faktauppgift. Texten får inte vara tom.",

        "backend.mail.fact_save_failed":
            "Sparandet avbröts. {count} nya kunskapsposter hann sparas. Försök igen.",
        "backend.mail.fact_save_success":
            "Sparade {count} nya kunskapsposter. Eventuella dubbletter hoppades över.",

        "backend.mail.file_missing":
            "Den valda filen finns inte.",
        "backend.mail.read_failed":
            "Filen kunde inte läsas.",
        "backend.mail.none_added":
            "Ingen ny kunskap lades till.",
        "backend.mail.import_success":
            "Importerade {count} kunskapsposter från mejlfil.",

        # Backend - answer generation
        "backend.answer.not_enough_info":
            "Det finns inte tillräcklig information i kunskapsbasen.",
        "backend.answer.failed":
            "Svaret kunde inte skapas. Försök igen.",

        # Backend - model loading
        "backend.model.load_failed":
            "Modellen kunde inte laddas.",

        # Backend - backup
        "backend.backup.export_failed":
            "Kunskapsbasen kunde inte exporteras.",
        "backend.backup.export_success":
            "Exporterade {count} kunskapsposter.",
        "backend.backup.import_success":
            "Importerade {imported} poster. Hoppade över {skipped} poster.",

        # Text parser.
        "text_parser.file_not_found":
            "Textfilen kunde inte hittas.",
        "text_parser.invalid_file_type":
            "Filen måste vara en TXT-fil.",
        "text_parser.invalid_encoding":
            "Textfilen kunde inte läsas som UTF-8.",
        "text_parser.read_failed":
            "Textfilen kunde inte läsas.",
        "text_parser.empty_file":
            "Textfilen är tom.",

        # Document parser.
        "document_parser.file_not_found":
            "DOCX-filen kunde inte hittas.",
        "document_parser.invalid_file_type":
            "Filen måste vara en DOCX-fil.",
        "document_parser.invalid_document":
            "Filen är inte ett giltigt DOCX-dokument.",
        "document_parser.no_text":
            "Ingen läsbar text hittades i DOCX-filen.",

        # PDF parser.
        "pdf_parser.file_not_found":
            "PDF-filen kunde inte hittas.",
        "pdf_parser.invalid_file_type":
            "Filen måste vara en PDF-fil.",
        "pdf_parser.no_text":
            "Ingen läsbar text hittades i PDF-filen. "
            "Filen kan innehålla skannade bilder.",

        # Mail parser.
        "mail_parser.file_not_found":
            "Mejlfilen kunde inte hittas.",
        "mail_parser.invalid_file_type":
            "Filen måste vara en EML- eller MSG-fil.",
        "mail_parser.empty_email":
            "Mejlet innehåller ingen text.",
        "mail_parser.read_failed":
            "Mejlfilen kunde inte läsas.",
        "mail_parser.no_body":
            "Ingen vanlig text eller HTML hittades i mejlet.",
        "mail_parser.decode_failed":
            "Mejltexten kunde inte avkodas.",
        "mail_parser.msg_read_failed":
            "MSG-filen kunde inte läsas.",

        # JSON importer.
        "json_importer.file_not_found":
            "Den valda backupfilen finns inte.",
        "json_importer.invalid_json":
            "Den valda filen innehåller inte giltig JSON.",
        "json_importer.invalid_root":
            "Backupfilen måste innehålla en lista med kunskapsposter.",
        "json_importer.invalid_entry":
            "Varje kunskapspost måste vara ett JSON-objekt.",
        "json_importer.missing_fields":
            "En eller flera kunskapsposter saknar obligatoriska fält.",

        # System tray.
        "tray.open": "Öppna",
        "tray.quit": "Avsluta",

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
        "settings.invalid_threshold": (
            "Similarity threshold must be a valid number between 0 and 1."
        ),

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

        # Header.
        "header.user_guide": "User guide",

        # Thinking
        "thinking.status": "Thinking…",

        # Chat input.
        "chat_input.placeholder": "Type your question here",
        "chat_input.send": "Send",

        # Chatview.
        "chat_view.welcome": "What would you like to know?",

        # Chat message.
        "chat_message.you": "You",
        "chat_message.review_facts": "Review suggested facts",
        "chat_message.source": "source",
        "chat_message.sources": "sources",
        "chat_message.entry": "entry",
        "chat_message.entries": "entries",
        "chat_message.click_for_details": "Click for details",

        # Model load.
        "model_load.title": "Change language model?",
        "model_load.warning": (
            "Loading a new model can take anywhere from a few seconds to several "
            "minutes depending on the model size, hardware, and whether the model "
            "is already available locally. If the model is missing, it may need "
            "to be downloaded first."
        ),
        "model_load.confirm": "Load model",

        # Mail review.
        "mail_review.title_prefix": "Review facts:",
        "mail_review.close": "Close review",
        "mail_review.close_keep": "Close and keep suggestions",
        "mail_review.discard": "Discard suggestions",
        "mail_review.save_selected": "Save selected facts",
        "mail_review.empty_selected_error":
            "Selected facts cannot be empty.",
        "mail_review.none_selected_error":
            "Select at least one fact to save.",
        "mail_review.original_email": "Original email",
        "mail_review.select_edit": "Select and edit facts",
        "mail_review.check_warning":
            "Check the suggestions against the original email. "
            "The AI may miss or misinterpret information.",
        "mail_review.no_facts":
            "The AI did not suggest any facts.",
        "mail_review.include_suggestion":
            "Include suggestion",

        # Mail preview.
        "mail_preview.title": "Preview email",
        "mail_preview.save_full": "Save entire email",
        "mail_preview.review_suggestions": "Review suggestions",
        "mail_preview.suggest_facts": "Suggest facts with AI",
        "mail_preview.preview_prefix": "Preview:",
        "mail_preview.close_preview": "Close preview",

        # Mail analysis.
        "mail_analysis.title": "Analyze email with AI?",
        "mail_analysis.warning": (
            "The AI analysis may take several minutes depending on the length "
            "of the email, the loaded model, and your computer's performance. "
            "You will be able to review and edit the suggestions before "
            "anything is saved."
        ),
        "mail_analysis.analyze": "Analyze email",

        # Main QML.
        "filedialog.select_mail": "Select an email",
        "filedialog.mail_files": "Email files (*.eml *.msg)",
        "filedialog.import_backup": "Import backup",
        "status.exporting": "Exporting…",
        "status.error_prefix": "Error:",
        "mail_status.analyzing": "Analyzing email…",
        "mail_status.analysis_failed":
            "The email could not be analyzed. Please try again.",
        "mail_status.analysis_done": "Email analysis is complete.",
        "mail_status.suggestions_to_review": "suggestions to review.",
        "mail_status.no_facts":
            "No facts were suggested.",
        "mail_status.review_finished":
            "Email review is complete.",
        "mail_status.analysis_of": "The analysis of email",
        "mail_status.is_done": "is complete.",

        # Document preview.
        "document_preview.title": "Review document",
        "document_preview.edit_hint":
            "Review and edit the text before saving.",

        # Document import errors.
        "document_import.invalid_encoding":
            "The text file could not be read. Save it as UTF-8 and try again.",
        "document_import.empty_file":
            "The text file is empty.",
        "document_import.read_failed":
            "The file could not be read. Check that it exists and can be opened.",

        # Document saving.
        "document_save.empty_text": "There is no text to save.",
        "document_save.saved": "The document text has been saved.",
        "document_save.already_exists":
            "The text already exists in the knowledge base.",
        "document_save.failed":
            "The document text could not be saved. Please try again.",
        "document_save.save_full": "Save as one entry",
        "document_save.single_tooltip":
            "Save the entire text as one knowledge entry",
        "document_save.save_chunks": "Save in chunks",
        "document_save.chunks_tooltip":
            "Save each paragraph as a separate entry",
        "document_save.chunks_saved": (
            "Saved {count} new knowledge entries. "
            "Any duplicates were skipped."
        ),
        "document_save.chunks_failed": (
            "Saving was interrupted. {count} new knowledge entries "
            "were saved before the error. Your text is still available. "
            "Please try again."
        ),
        "document_analysis.failed":
            "The document could not be analyzed. Please try again.",
        "document_analysis.busy":
            "Wait until the current task has finished.",
        "document_analysis.review_pending":
            "Review and save or discard the document suggestions first.",
        "document_analysis.title": "Analyze document with AI?",
        "document_analysis.warning": (
            "The AI analysis may take several minutes depending on the "
            "text length, the loaded model and your computer's performance. "
            "You can review and edit the suggestions before anything is saved."
        ),
        "document_analysis.analyze": "Analyze document",
        "document_preview.suggest_facts": "Suggest facts with AI",
        
        # Document review.
        "document_review.original_text": "Analyzed text",
        "document_review.check_warning": (
            "Check the suggestions against the document text. "
            "The AI may miss or misinterpret information."
        ),

        "document_review.no_pending":
            "There are no document suggestions to save.",
        "document_review.invalid_selection":
            "Select at least one fact. Selected passages cannot be empty.",
        "document_review.saved": (
            "Saved {count} new knowledge entries. "
            "Any duplicates were skipped."
        ),
        "document_review.save_failed": (
            "Saving was interrupted. {count} new knowledge entries "
            "were saved before the error. Your review is still available. "
            "Please try again."
        ),

        "document_analysis.analyzing": "Analyzing document…",
        "document_analysis.ready":
            "Analysis complete. Review the suggestions before saving.",
        "document_analysis.no_facts":
            "Analysis complete. No facts were suggested.",
        "document_review.finished": "Document review is complete.",

        # Backend - model
        "backend.model.busy":
            "Wait until the current task has finished.",
        "backend.model.loading":
            "Loading model: {model}",
        "backend.model.loaded":
            "Model loaded: {model}",

        # Backend - RAG
        "backend.rag.top_k_min":
            "Top-K must be at least 1.",
        "backend.rag.threshold_range":
            "The similarity threshold must be between 0.0 and 1.0.",
        "backend.rag.updated":
            "RAG settings have been updated.",

        # Backend - question processing
        "backend.reply.busy":
            "The model is busy. Wait until the current task has finished.",

        # Backend - knowledge editing
        "backend.knowledge.empty_text":
            "The text cannot be empty.",
        "backend.knowledge.duplicate":
            "An entry with the same text already exists.",
        "backend.knowledge.updated":
            "The knowledge entry has been updated.",
        "backend.knowledge.not_found":
            "The knowledge entry could not be found.",
        "backend.knowledge.deleted":
            "The knowledge entry has been deleted.",

        # Backend - source deletion
        "backend.source_delete.none":
            "No knowledge entries could be deleted.",
        "backend.source_delete.success":
            "{count} knowledge entries were deleted.",

        # Backend - manual knowledge
        "backend.manual.empty":
            "No knowledge was added.",
        "backend.manual.added":
            "Knowledge added.",
        "backend.manual.no_new":
            "No new knowledge was added.",

        # Backend - dropped documents
        "backend.drop.local_only":
            "Drop a local file from your computer.",
        "backend.drop.not_found":
            "The file could not be found. Folders cannot be imported.",
        "backend.drop.unsupported":
            "The file type is not supported. Choose TXT, PDF, DOCX, EML, or MSG.",

        # Backend - document import
        "backend.import.file_missing":
            "The selected file does not exist.",
        "backend.import.none_added":
            "No new knowledge was added.",

        "backend.import.txt_success":
            "Imported {count} knowledge entries from text file.",
        "backend.import.docx_success":
            "Imported {count} knowledge entries from DOCX file.",
        "backend.import.pdf_success":
            "Imported {count} knowledge entries from PDF file.",

        # Backend - mail
        "backend.mail.empty_save":
            "There is no email to save.",
        "backend.mail.save_failed":
            "The email could not be saved. Please try again.",
        "backend.mail.saved":
            "The email has been saved.",
        "backend.mail.duplicate":
            "The email already exists in the knowledge base.",

        "backend.mail.empty_analysis":
            "There is no email to analyze.",
        "backend.mail.busy":
            "Wait until the current task has finished.",
        "backend.mail.review_pending":
            "Review or discard the previous suggestions first.",
        "backend.mail.analyzing":
            "Analyzing the email…",
        "backend.mail.analysis_ready":
            "Email analysis is complete. Review the suggestions before saving.",
        "backend.mail.analysis_failed":
            "The email could not be analyzed. Please try again.",

        "backend.mail.no_review":
            "There are no email suggestions to review.",
        "backend.mail.no_facts_to_save":
            "There are no email suggestions to save.",
        "backend.mail.invalid_selection":
            "Select at least one fact. The text cannot be empty.",

        "backend.mail.fact_save_failed":
            "Saving was interrupted. {count} new knowledge entries were saved before the error. Please try again.",
        "backend.mail.fact_save_success":
            "Saved {count} new knowledge entries. Any duplicates were skipped.",

        "backend.mail.file_missing":
            "The selected file does not exist.",
        "backend.mail.read_failed":
            "The file could not be read.",
        "backend.mail.none_added":
            "No new knowledge was added.",
        "backend.mail.import_success":
            "Imported {count} knowledge entries from email file.",

        # Backend - answer generation
        "backend.answer.not_enough_info":
            "There is not enough information in the knowledge base.",
        "backend.answer.failed":
            "The answer could not be generated. Please try again.",

        # Backend - model loading
        "backend.model.load_failed":
            "The model could not be loaded.",

        # Backend - backup
        "backend.backup.export_failed":
            "The knowledge base could not be exported.",
        "backend.backup.export_success":
            "Exported {count} knowledge entries.",
        "backend.backup.import_success":
            "Imported {imported} entries. Skipped {skipped} entries.",

        # Text parser.
        "text_parser.file_not_found":
            "The text file could not be found.",
        "text_parser.invalid_file_type":
            "The file must be a TXT file.",
        "text_parser.invalid_encoding":
            "The text file could not be read as UTF-8.",
        "text_parser.read_failed":
            "The text file could not be read.",
        "text_parser.empty_file":
            "The text file is empty.",

        # Document parser.
        "document_parser.file_not_found":
            "The DOCX file could not be found.",
        "document_parser.invalid_file_type":
            "The file must be a DOCX file.",
        "document_parser.invalid_document":
            "The file is not a valid DOCX document.",
        "document_parser.no_text":
            "No readable text was found in the DOCX file.",

        # PDF parser.
        "pdf_parser.file_not_found":
            "The PDF file could not be found.",
        "pdf_parser.invalid_file_type":
            "The file must be a PDF file.",
        "pdf_parser.no_text":
            "No readable text was found in the PDF file. "
            "The file may contain scanned images.",

        # Mail parser.
        "mail_parser.file_not_found":
            "The email file could not be found.",
        "mail_parser.invalid_file_type":
            "The file must be an EML or MSG file.",
        "mail_parser.empty_email":
            "The email contains no text.",
        "mail_parser.read_failed":
            "The email file could not be read.",
        "mail_parser.no_body":
            "No plain text or HTML was found in the email.",
        "mail_parser.decode_failed":
            "The email text could not be decoded.",
        "mail_parser.msg_read_failed":
            "The MSG file could not be read.",

        # JSON importer.
        "json_importer.file_not_found":
            "The selected backup file does not exist.",
        "json_importer.invalid_json":
            "The selected file does not contain valid JSON.",
        "json_importer.invalid_root":
            "The backup file must contain a list of knowledge entries.",
        "json_importer.invalid_entry":
            "Each knowledge entry must be a JSON object.",
        "json_importer.missing_fields":
            "One or more knowledge entries are missing required fields.",

        # System tray.
        "tray.open": "Open",
        "tray.quit": "Exit",
        
    },
}

def translate(key: str, language: str) -> str:
        """Helper function to make Python able to use the dictionary."""
        return TRANSLATIONS.get(
            language,
            TRANSLATIONS["sv"]
        ).get(key, key)


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
        return translate(key, language)


    
    
