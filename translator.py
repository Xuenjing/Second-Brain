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
        "backend.manual.save_failed":
            "Kunskapen kunde inte sparas. Försök igen.",

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

        # User guide
        "help.title": "Användarguide",
        "help.close": "Stäng användarguiden",
        "help.intro": (
            "Second Brain hjälper dig att spara kunskap och ställa frågor "
            "om informationen."
        ),

        "help.add_heading": "Lägg till kunskap",
        "help.add_body": (
            "Öppna Lägg till kunskap. Skriv eller klistra in information "
            "och klicka på disketten för att spara.\n\n"
            "Tom text sparas inte. Dubbletter med samma text, även med "
            "skillnader i blanksteg, hoppas över."
        ),

        "help.documents_heading": "Importera och granska dokument",
        "help.documents_body": (
            "Importera en TXT-, PDF- eller DOCX-fil med filknapparna "
            "i Lägg till kunskap, eller dra filen till den markerade "
            "släppytan. Släpp en fil åt gången.\n\n"
            "Dokumentets text visas före sparande och kan redigeras. "
            "Välj sedan ett av tre alternativ:\n\n"
            "Överlappande dokument – Spara uppdelat: sparar texten "
            "som flera kunskapsposter. TXT delas vid tomma rader. "
            "DOCX delas vid stycken och tabeller. PDF delas utifrån "
            "sidgränser och stycken, med grundläggande tabellhantering.\n\n"
            "Disketten – Spara som en post: sparar hela den granskade "
            "texten som en enda kunskapspost.\n\n"
            "Hjärnan – Föreslå fakta med AI: låter den laddade "
            "språkmodellen föreslå fakta. Analysen kan ta flera minuter. "
            "Stora dokument kan ta lång tid eller misslyckas.\n\n"
            "Öppna granskningen när analysen är klar. Jämför förslagen "
            "med texten, redigera vid behov och avmarkera sådant du inte "
            "vill spara. Spara valda förslag eller kasta granskningen. "
            "Analysen i sig sparar inga poster och kan ge noll förslag.\n\n"
            "TXT-filer behöver vara UTF-8-kodade. PDF-import kräver "
            "läsbar text; skannade bilder behandlas inte med OCR. "
            "Kontrollera alltid importerad text och tabeller."
        ),

        "help.mail_heading": "Importera och granska mejl",
        "help.mail_body": (
            "Importera en EML- eller MSG-fil med mejlknappen i "
            "Lägg till kunskap, eller släpp filen på släppytan.\n\n"
            "Granska mejltexten före sparande. Du kan spara hela "
            "mejltexten eller klicka på hjärnan för att få AI-förslag. "
            "Analysen använder den laddade språkmodellen och kan "
            "ta flera minuter.\n\n"
            "När analysen är klar öppnar du granskningen. Jämför "
            "förslagen med originalet, redigera och välj bort sådant "
            "du inte vill spara. Spara valda förslag eller kasta "
            "granskningen. Ett mejl utan användbara fakta kan ge "
            "noll förslag.\n\n"
            "Kontrollera särskilt namn, datum, kontaktuppgifter och "
            "formuleringar med exempelvis inte eller får inte. "
            "AI:n kan också ta med onödiga fraser."
        ),

        "help.chat_heading": "Ställ frågor och granska källor",
        "help.chat_body": (
            "Skriv din fråga i chattfältet och klicka på Skicka. "
            "Vänta medan modellen arbetar.\n\n"
            "Second Brain söker efter relevant sparad kunskap och "
            "använder den som underlag för svaret. Tydliga frågor med "
            "namn eller andra detaljer gör det lättare att hitta rätt "
            "information.\n\n"
            "Hovra över informationsikonen vid ett svar för att se "
            "en sammanfattning av källorna. Klicka på ikonen för "
            "att granska kunskapsposterna som användes. Där kan du "
            "också söka och undersöka fler poster.\n\n"
            "AI:n kan missa eller misstolka information. Kontrollera "
            "viktiga uppgifter mot källorna."
        ),

        "help.knowledge_heading": "Visa och hantera kunskap",
        "help.knowledge_body": (
            "Öppna Visa kunskapsposter för att se sparad information. "
            "Använd sökfältet, filtren för källtyp och sorteringen "
            "för att hitta poster.\n\n"
            "Antalet ovanför sökfältet visar hur många poster som "
            "matchar det aktuella urvalet. Varje post visar också "
            "sin källa och tidpunkt.\n\n"
            "Använd pennan för att redigera en post och papperskorgen "
            "för att ta bort den. Bekräfta borttagningen eller välj "
            "Avbryt för att behålla posten.\n\n"
            "Växla till Visa källor för att hantera poster per källa. "
            "Ta bort källa tar bort samtliga kunskapsposter från "
            "den valda källan efter bekräftelse. "
            "Borttagningen kan inte ångras."
        ),

        "help.model_heading": "Byt språkmodell",
        "help.model_body": (
            "Välj en modell i modellistan i huvudfönstret och klicka "
            "på Ladda modell. Bekräfta modellbytet och vänta tills "
            "laddningen är klar. Att bara välja ett namn i listan "
            "laddar inte modellen.\n\n"
            "Den laddade modellen används för chatsvar och "
            "AI-analys av dokument och mejl.\n\n"
            "Första gången kan modellen behöva laddas ner, vilket "
            "kräver internetanslutning. Laddnings- och svarstider "
            "beror på modellens storlek och datorns prestanda."
        ),

        "help.rag_heading": "Ändra RAG-inställningar",
        "help.rag_body": (
            "Öppna inställningarna med kugghjulet.\n\n"
            "Top-K anger hur många kunskapsposter som högst väljs "
            "ut som underlag för ett svar.\n\n"
            "Likhetströskeln anger hur väl informationen behöver "
            "matcha frågan. Värdet ska vara mellan 0 och 1. "
            "En högre tröskel gör urvalet striktare och kan ge "
            "färre träffar. Både decimalpunkt och decimalkomma "
            "kan användas.\n\n"
            "Klicka på Spara RAG-inställningar för att spara. "
            "Ogiltiga värden ger ett felmeddelande och sparas inte.\n\n"
            "Återställ standardvärden återställer och sparar "
            "Top-K 5 och likhetströskeln 0.82. Sparade "
            "RAG-inställningar finns kvar efter omstart."
        ),

        "help.settings_heading": "Språk, utseende och säkerhetskopiering",
        "help.settings_body": (
            "I inställningarna kan du välja svenska eller engelska "
            "och växla mellan ljust och mörkt tema. Användarguiden "
            "följer det valda språket. Språkvalet översätter "
            "inte innehållet i dina sparade kunskapsposter.\n\n"
            "Använd Exportera databas för att spara en säkerhetskopia "
            "som JSON-fil. Använd Importera databas för att läsa "
            "in en sådan fil. Importen lägger till poster i den "
            "befintliga kunskapsbasen. Dubbletter kan hoppas över."
        ),

        "help.tray_heading": "Stäng och avsluta",
        "help.tray_body": (
            "När du stänger huvudfönstret fortsätter appen att "
            "köras i systemfältet vid klockan.\n\n"
            "Högerklicka på Second Brains ikon och välj Öppna "
            "för att visa fönstret igen, eller Avsluta för "
            "att stänga programmet helt."
        ),

        "help.online_manual": "Öppna hela manualen i webbläsaren",

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
        "backend.manual.save_failed":
            "The knowledge could not be saved. Please try again.",

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

        # User guide
        "help.title": "User guide",
        "help.close": "Close the user guide",
        "help.intro": (
            "Second Brain helps you store knowledge and ask questions "
            "about the information."
        ),

        "help.add_heading": "Add knowledge",
        "help.add_body": (
            "Open Add knowledge. Type or paste information and click "
            "the floppy disk to save it.\n\n"
            "Empty text is not saved. Duplicate text, including text "
            "that differs only in whitespace, is skipped."
        ),

        "help.documents_heading": "Import and review documents",
        "help.documents_body": (
            "Import a TXT, PDF or DOCX file using the file buttons "
            "in Add knowledge, or drag the file onto the marked "
            "drop area. Drop one file at a time.\n\n"
            "The document text is displayed for review and can be "
            "edited before saving. Choose one of three options:\n\n"
            "Overlapping documents – Save in chunks: saves the text "
            "as several knowledge entries. TXT is split at blank lines. "
            "DOCX is split at paragraph and table boundaries. PDF "
            "is split using page and paragraph boundaries, with "
            "basic table handling.\n\n"
            "Floppy disk – Save as one entry: saves all the reviewed "
            "text as a single knowledge entry.\n\n"
            "Brain – Suggest facts with AI: uses the loaded language "
            "model to suggest facts. Analysis can take several minutes. "
            "Large documents may take a long time or fail to complete.\n\n"
            "Open the review when analysis is complete. Compare the "
            "suggestions with the text, edit them if needed and uncheck "
            "anything you do not want to save. Save the selected "
            "suggestions or discard the review. Analysis itself "
            "does not save any entries and may produce no suggestions.\n\n"
            "TXT files must use UTF-8 encoding. PDF import requires "
            "readable text; scanned images are not processed using OCR. "
            "Always check imported text and tables."
        ),

        "help.mail_heading": "Import and review emails",
        "help.mail_body": (
            "Import an EML or MSG file using the email button in "
            "Add knowledge, or drop the file onto the drop area.\n\n"
            "Review the email text before saving. You can save the "
            "entire email text or click the brain to get AI suggestions. "
            "Analysis uses the loaded language model and can take "
            "several minutes.\n\n"
            "When analysis is complete, open the review. Compare the "
            "suggestions with the original, edit them and uncheck "
            "anything you do not want to save. Save the selected "
            "suggestions or discard the review. An email without "
            "useful facts may produce no suggestions.\n\n"
            "Pay particular attention to names, dates, contact details "
            "and wording such as not or must not. The AI may also "
            "include unnecessary phrases."
        ),

        "help.chat_heading": "Ask questions and inspect sources",
        "help.chat_body": (
            "Type your question in the chat field and click Send. "
            "Wait while the model processes your question.\n\n"
            "Second Brain searches for relevant stored knowledge "
            "and uses it as context for the answer. Clear questions "
            "with names or other details make it easier to find "
            "the right information.\n\n"
            "Hover over the information icon beside an answer to "
            "see a summary of its sources. Click the icon to inspect "
            "the knowledge entries used. You can also search "
            "and explore additional entries there.\n\n"
            "The AI may miss or misinterpret information. Check "
            "important details against the sources."
        ),

        "help.knowledge_heading": "View and manage knowledge",
        "help.knowledge_body": (
            "Open View knowledge entries to see stored information. "
            "Use the search field, source-type filters and sorting "
            "to find entries.\n\n"
            "The count above the search field shows how many entries "
            "match the current selection. Each entry also displays "
            "its source and timestamp.\n\n"
            "Use the pencil to edit an entry and the trash can "
            "to delete it. Confirm deletion or select Cancel "
            "to keep the entry.\n\n"
            "Switch to Show sources to manage entries by source. "
            "Delete source removes all knowledge entries from "
            "the selected source after confirmation. "
            "This deletion cannot be undone."
        ),

        "help.model_heading": "Change the language model",
        "help.model_body": (
            "Select a model from the dropdown in the main window "
            "and click Load model. Confirm the change and wait "
            "until loading is complete. Selecting a name in "
            "the dropdown does not load the model by itself.\n\n"
            "The loaded model is used for chat answers and "
            "AI analysis of documents and emails.\n\n"
            "The model may need to be downloaded the first time, "
            "which requires an internet connection. Loading "
            "and response times depend on the model size "
            "and your computer's performance."
        ),

        "help.rag_heading": "Change RAG settings",
        "help.rag_body": (
            "Open settings using the gear icon.\n\n"
            "Top-K sets the maximum number of knowledge entries "
            "selected as context for an answer.\n\n"
            "Similarity threshold determines how closely information "
            "needs to match the question. The value must be between "
            "0 and 1. A higher threshold makes selection stricter "
            "and may return fewer matches. You can use either "
            "a decimal point or a decimal comma.\n\n"
            "Click Save RAG settings to save your changes. "
            "Invalid values display an error and are not saved.\n\n"
            "Reset to defaults restores and saves Top-K 5 "
            "and similarity threshold 0.82. Saved RAG settings "
            "are retained after restarting."
        ),

        "help.settings_heading": "Language, appearance and backup",
        "help.settings_body": (
            "In settings, you can select Swedish or English "
            "and switch between light and dark appearance. "
            "The user guide follows the selected language. "
            "Changing the interface language does not translate "
            "the content of your stored knowledge entries.\n\n"
            "Use Export database to save a backup as a JSON file. "
            "Use Import database to read a file of that type. "
            "Importing adds entries to the existing knowledge base. "
            "Duplicates may be skipped."
        ),

        "help.tray_heading": "Close and exit",
        "help.tray_body": (
            "Closing the main window leaves the application "
            "running in the system tray near the clock.\n\n"
            "Right-click the Second Brain icon and select Open "
            "to show the window again, or Exit to close "
            "the application completely."
        ),

        "help.online_manual": "Open the full manual in your browser",
        
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