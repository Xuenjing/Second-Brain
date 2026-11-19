# Developer Guide

This document provides a technical overview of the Second Brain project for developers who want to understand, maintain or extend the application.

Second Brain is a local desktop knowledge-base application built with Python and PySide6/QML. It uses retrieval-augmented generation (RAG), semantic embeddings and local language models to answer questions based on information stored in the user's local knowledge base.

---

## Architecture

The application is divided into several main layers:

```text
QML user interface
        ↓
Python backend
        ↓
Retrieval / knowledge management
        ↓
SQLite database
        ↓
Embedding model + local language model
```

The QML interface communicates with the Python backend through Qt signals and slots.

The backend coordinates:

- knowledge storage
- document and email import
- retrieval
- prompt construction
- language-model generation
- settings
- backup and restore
- communication with the QML interface

Long-running language-model generation is performed outside the main UI flow to avoid blocking the interface.

---

## Project Structure

The most important parts of the project are:

```text
Second Brain/
│
├── main.py
├── backend.py
├── database.py
├── retrieval.py
├── translator.py
├── requirements.txt
│
├── imports/
│   ├── text_parser.py
│   ├── text_importer.py
│   ├── document_parser.py
│   ├── document_importer.py
│   ├── pdf_parser.py
│   ├── pdf_importer.py
│   ├── mail_parser.py
│   └── mail_importer.py
│
├── llm/
│   ├── local_provider.py
│   └── external_provider.py
│
├── qml/
│   ├── main.qml
│   ├── components/
│   └── dialogs/
│
├── tests/
│
├── experiments/
│
├── docs/
│
├── SecondBrain.spec
└── SecondBrain.iss
```

### `main.py`

Application entry point.

Responsible for starting Qt, creating the backend and loading the QML interface.

### `backend.py`

Acts as the main bridge between QML and the application logic.

Responsibilities include:

- receiving questions from the UI
- coordinating retrieval
- building RAG prompts
- calling the language model
- returning answers and source references
- knowledge management
- document and email import
- settings
- backup operations

### `database.py`

Handles SQLite storage and retrieval.

The database contains stored knowledge together with:

- text
- source
- creation timestamp
- embedding

The database is stored in the current user's application-data directory:

```text
%LOCALAPPDATA%\SecondBrain\knowledge.db
```

The directory is created automatically when the application initializes.

This keeps user data separate from the application installation directory.

### `retrieval.py`

Handles retrieval of relevant knowledge for user questions.

Retrieval combines semantic similarity with lightweight lexical / identifier matching.

The default configuration currently uses:

```text
Top-K: 5
Similarity threshold: 0.82
```

These values can also be changed through the application settings.

---

## RAG Pipeline

The main question-answering flow is:

```text
User question
      ↓
Question embedding
      ↓
Knowledge retrieval
      ↓
Relevant knowledge entries
      ↓
Prompt + retrieved context
      ↓
Local language model
      ↓
Generated answer
      ↓
Answer + source references
```

The model receives only retrieved context that is considered relevant to the question.

Prompt instructions are used to:

- avoid unsupported answers
- respect negation
- avoid mixing information between entities
- answer in the same language as the user's question
- report insufficient information when the required answer is not present

Source references are returned together with the generated answer so the user can inspect the underlying knowledge.

---

## Embeddings and Retrieval

Embeddings are generated using:

```text
intfloat/multilingual-e5-small
```

Stored knowledge entries contain serialized embeddings in the SQLite database.

When a question is asked:

1. the question is embedded
2. stored entries are compared against the question
3. relevant entries are ranked
4. threshold filtering is applied
5. the most relevant results are passed to the language model

Retrieval quality has been tested separately from generation quality to distinguish retrieval errors from language-model errors.

The retrieval pipeline has also been evaluated using larger heterogeneous datasets containing approximately 1,200 and 10,000 knowledge entries.

---

## Language Models

The default local language model is:

```text
Qwen/Qwen3-1.7B
```

Additional Qwen models are available through the application's model selector.

The 1.7B model is used as the recommended default because it provides a useful balance between answer quality and CPU performance.

Models are loaded through the local provider implementation in:

```text
llm/local_provider.py
```

The provider applies the model's chat template and disables Qwen thinking mode for normal application responses.

Models are downloaded through Hugging Face when required and stored in the user's local Hugging Face cache.

An experimental external-provider implementation also exists but is not part of the normal production workflow.

---

## Knowledge and Document Import

Second Brain supports several input formats.

### Manual knowledge

Users can add knowledge directly through the interface.

The text is embedded and stored together with a manual source identifier.

### TXT

TXT files are read as UTF-8 text and divided into chunks before storage.

### DOCX

DOCX parsing supports:

- paragraphs
- table extraction
- empty-content validation
- source tracking

### PDF

PDF parsing supports text-based PDFs.

The implementation performs page-based text extraction and basic chunking.

PDF parsing is necessarily heuristic because PDF files do not contain document structure in the same way as DOCX documents.

Scanned or image-only PDFs are currently not processed using OCR.

### EML and MSG

Saved email files can be imported and reviewed.

Email parsing extracts relevant message content and metadata.

Documents and emails can also be passed through AI-assisted analysis before information is stored in the knowledge base.

Generated suggestions are reviewed by the user before being saved.

---

## Knowledge Management

Stored knowledge can be:

- searched
- filtered
- sorted
- edited
- deleted individually
- deleted by source

Duplicate prevention is implemented at the database layer using normalized text comparison.

Original text formatting is preserved when stored.

---

## Settings

Application settings are persisted using Qt settings.

Configurable options include:

- interface language
- appearance
- selected language model
- Top-K retrieval value
- similarity threshold

The selected interface language does not determine the language of generated answers.

The answer language is based on the language of the user's question.

---

## Localization

Localization is handled through:

```text
translator.py
```

The application currently supports:

- Swedish
- English

Translation keys are stored centrally and accessed through a translator object exposed to QML.

Backend-generated user-facing messages use the same translation system.

This allows the QML and Python sides of the application to use the same language selection.

---

## Backup and Restore

The knowledge database can be exported to JSON.

Backup files can later be imported into the application.

Backup functionality is intended for:

- data migration
- manual backup
- restoring knowledge after data removal
- transferring knowledge between installations

---

## Testing

Automated tests cover several core parts of the application.

Areas include:

- database operations
- duplicate handling
- retrieval
- TXT import
- DOCX import
- PDF import
- backup/export functionality

Tests are also executed through GitHub Actions.

The project additionally contains evaluation and benchmark material under:

```text
experiments/
```

Older investigations and benchmark datasets are stored under:

```text
experiments/archive/
```

### Running tests

Activate the project's virtual environment and run the relevant test suite using the project's existing test commands.

A clean environment can be created from:

```text
requirements.txt
```

The runtime requirements have been verified by installing them into a fresh virtual environment and running the application from that environment.

---

## Runtime Dependencies

The main runtime dependencies are defined in:

```text
requirements.txt
```

The direct application dependencies currently include:

```text
PySide6
NumPy
scikit-learn
sentence-transformers
PyTorch
Transformers
extract-msg
python-docx
pypdf
```

Indirect dependencies are installed automatically by `pip`.

Experimental provider code may require additional packages that are not part of the normal runtime environment.

---

## Packaging

Second Brain is packaged for Windows in two stages.

### PyInstaller

PyInstaller creates a standalone application bundle.

Configuration is stored in:

```text
SecondBrain.spec
```

The build includes:

- Python application code
- required Python dependencies
- QML files
- application assets

The current build uses a directory-based distribution rather than a single-file executable.

Build with:

```bash
pyinstaller --clean SecondBrain.spec
```

The resulting application is created under:

```text
dist/SecondBrain/
```

### Inno Setup

Inno Setup packages the PyInstaller output into a normal Windows installer.

Configuration is stored in:

```text
SecondBrain.iss
```

The installer provides:

- installation under Program Files
- Start menu shortcut
- optional desktop shortcut
- uninstall support

The compiled installer is created as:

```text
SecondBrain-Setup.exe
```

Generated build directories such as `build/`, `dist/` and `installer/` are not intended to be version controlled.

Release installers should instead be distributed through GitHub Releases.

---

## User Data

Application installation files and user data are intentionally separated.

Program files are installed under Windows Program Files.

The knowledge database is stored under:

```text
%LOCALAPPDATA%\SecondBrain\
```

This means uninstalling or replacing the application does not automatically remove the user's knowledge database.

---

## Documentation

User-facing documentation is published separately using Zensical and GitHub Pages.

The user manual contains instructions for:

- installation
- adding knowledge
- asking questions
- managing knowledge
- AI-assisted analysis
- settings
- backup and restore

The developer guide focuses instead on the internal structure and maintenance of the application.

---

## Known Limitations

Current known limitations include:

- PDF structure extraction is heuristic
- local language-model quality is limited by model size and available hardware
- model loading and first-time downloads may take time
- some complex questions may fail even when retrieval is correct
- the experimental external-provider implementation is not part of the standard application workflow

---

## Future Development

Possible future improvements include:

- additional document formats
- improved PDF structure extraction
- further local-model evaluation
- improved performance on very large knowledge bases
- external AI-provider integrations
- expanded source inspection and navigation

These areas are optional future work rather than requirements for the current v1.0 release.