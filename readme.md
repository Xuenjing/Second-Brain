# Second Brain

Second Brain is a desktop application designed to provide a local knowledge base where users can store information and later retrieve it through natural-language questions.

The application combines local knowledge storage, semantic search, retrieval and language models to provide answers based on information stored in the knowledge base.

---

## Current functionality

The current prototype supports:

- Manual knowledge input through the user interface
- Import of `.txt` files
- Import of `.docx` documents
- Import of `.pdf` documents
- Import of .eml Email files
- Paragraph-based document chunking
- Basic table-aware chunking for DOCX and PDF documents
- Local knowledge storage using SQLite
- Storage of source information and creation timestamps
- Duplicate prevention for stored knowledge
- Embedding generation for stored knowledge
- Hybrid retrieval combining semantic similarity with lightweight lexical / identifier matching
- Top-k retrieval with similarity-threshold filtering
- Retrieval-Augmented Generation (RAG)
- Local language-model integration
- Background LLM generation to avoid blocking the interface
- Knowledge-base viewer
- Search within stored knowledge
- Filtering by source type:
  - TXT
  - DOCX
  - PDF
  - Manual entries
- Sorting knowledge by creation date
- Combined search, filtering and sorting
- Editing stored knowledge
- Deleting stored knowledge
- System tray support
- Communication between QML and Python using Qt signals and slots
- Automated unit tests
- GitHub Actions for continuous test execution
- Benchmark and experiment scripts for retrieval, embeddings and language models
- Scalability testing with knowledge bases containing 1,200 and 10,000 entries
- JSON export of the knowledge database
- Source references / traceability for generated answers
- Opening a referenced knowledge entry from an answer source
- TXT-import tests
- PDF-import tests

---

## Architecture

Second Brain is divided into several main components.

### User interface

The user interface is built with QML and Qt Quick.

The QML interface is divided into reusable components and dialogs, while main.qml primarily coordinates application state, backend communication and the main layout.

QML communicates with the Python backend through PySide6 signals and slots.

The interface currently contains functionality for:

- Asking questions
- Viewing generated answers
- Adding knowledge manually
- Importing supported document types
- Viewing stored knowledge
- Searching stored knowledge
- Filtering by source type
- Sorting by creation date
- Editing knowledge
- Deleting knowledge
- Selecting between planned/local model options in the interface
- Viewing the sources used for generated answers
- Opening referenced knowledge entries

---

### Backend

The Python backend handles communication between the user interface and the underlying application logic.

Its responsibilities currently include:

- Receiving user questions
- Coordinating hybrid retrieval
- Building RAG context
- Sending context and questions to the language model
- Returning generated answers to QML
- Handling background LLM generation
- Adding knowledge manually
- Importing TXT, DOCX, PDF and EML files
- Searching, filtering and sorting stored knowledge
- Editing stored knowledge
- Deleting stored knowledge
- Formatting database entries for display in QML
- Exporting the knowledge database to JSON
- Providing source metadata together with generated answers

Document parsing and importing are separated from the main backend where appropriate to keep individual components smaller and easier to test.

---

## Knowledge storage

SQLite is currently used as the local knowledge database.

Knowledge entries can contain:

- Text
- Source
- Creation timestamp
- Embedding

Duplicate text entries are prevented by the database.

The database is initialized when the backend starts to ensure that the required schema exists before the application attempts to access stored knowledge.

Sources currently include manually created entries and imported file names.

---

## Document import

### TXT

UTF-8 text files can be imported and split into paragraph-based chunks.

Each chunk is embedded and stored separately.

### DOCX

DOCX documents are parsed using a dedicated document parser.

Current support includes:

- Paragraph extraction
- Ignoring empty paragraphs
- Table extraction
- Storing each table as a combined multiline chunk
- Validation of missing, invalid or incorrectly typed files

A current limitation is that paragraph and table extraction does not necessarily preserve the exact original block order of the Word document.

### PDF

PDF documents are parsed using `pypdf`.

Current support includes:

- Page-by-page text extraction
- Layout-based extraction
- Paragraph-based chunking
- Basic detection of table-like text using whitespace patterns
- Grouping table-like content into larger chunks

The current PDF implementation is intended primarily for text-based PDFs.

Scanned or image-only PDFs are not currently processed using OCR.

PDF parsing remains heuristic because PDF files do not contain document structure in the same way as DOCX files.

### EML

Saved email files can be imported into the knowledge base.

Email parsing and database importing are separated into dedicated
parser and importer modules, following the same general structure
used for the other supported document formats.

---

## Embeddings and retrieval

Embeddings are currently generated using:

`intfloat/multilingual-e5-small`

The user's question is converted into an embedding and compared with stored knowledge using cosine similarity.

Production retrieval uses a hybrid approach where semantic similarity remains the main ranking signal, while lightweight lexical / identifier matching can provide an additional signal when relevant.

Relevant entries are selected using a similarity threshold and top-k retrieval.

The current similarity threshold is:

`0.82`

This threshold was selected based on earlier retrieval experiments.

The current default top-k value is:

`5`

Retrieval quality is evaluated separately from language-model answer quality. Recent tests indicate that retrieval is generally reliable, while several remaining answer errors originate in generation rather than retrieval.



---

## Language model 

The current local language model is:

`Qwen/Qwen3-1.7B`

Qwen3-1.7B remains the current default because it provides the best overall balance between answer quality and CPU performance among the tested models.

The model was selected after benchmarking:

- `Qwen/Qwen3-0.6B`
- `Qwen/Qwen3-1.7B`
- `Qwen/Qwen3-4B-Instruct-2507`

Earlier tests showed that:

- Qwen3-0.6B was faster but produced weaker answers on some more demanding questions
- Qwen3-4B generally produced stronger answers but required considerably more generation time
- Qwen3-1.7B provided a useful balance between answer quality and CPU performance

Qwen thinking mode is explicitly disabled through the model's chat template.

The language model is accessed through a provider class rather than directly from the rest of the application. This makes it easier to replace the current local model with another local model or another provider in the future.

An OpenAI-compatible external-provider prototype has also been tested experimentally.

Evaluation of the complete RAG pipeline has shown that some remaining answer errors occur even when the correct knowledge entry is present in the retrieved context, indicating generation limitations rather than retrieval failure.

Therefore, answer quality and model selection are still under evaluation.

---

## RAG workflow

The current end-to-end question flow is:

```text
User question
      ↓
QML interface
      ↓
Python backend
      ↓
Hybrid retrieval
      ↓
Relevant knowledge chunks
      ↓
Prompt + retrieved context
      ↓
Language model
      ↓
Generated answer
      ↓
QML interface
```

The language model is instructed to answer using the retrieved context and avoid inventing information that is not available in the supplied knowledge.

Retrieval results used as context are also returned to the interface as answer sources. Users can inspect these sources and open the corresponding stored knowledge entry.

---

## Knowledge view

Stored knowledge can currently be searched, filtered and sorted.

Source filters currently support:

- TXT
- DOCX
- PDF
- Manual entries

The filters can be combined.

For example, a user can display only DOCX and PDF knowledge while simultaneously searching for a term and sorting the results by creation date.

Knowledge-view state is refreshed through a shared QML-to-backend flow so that searching, filtering, sorting, editing and deleting remain consistent with the currently selected view.

---

## Current project structure

The project currently contains components such as:

```text
Second Brain/
│
├── main.py
├── backend.py
├── database.py
├── exporter.py
├── performance.py
├── retrieval.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── imports/
│   ├── __init__.py
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
│   ├── __init__.py
│   ├── local_provider.py
│   └── external_provider.py
│
├── qml/
│   ├── main.qml
│   │
│   ├── components/
│   │   ├── ChatInput.qml
│   │   ├── ChatMessage.qml
│   │   ├── ChatView.qml
│   │   ├── Header.qml
│   │   ├── MainToolbar.qml
│   │   └── ThinkingIndicator.qml
│   │
│   └── dialogs/
│       ├── DeleteKnowledgeDialog.qml
│       ├── EditKnowledgeDialog.qml
│       ├── KnowledgeDialog.qml
│       ├── KnowledgeViewDialog.qml
│       ├── SettingsDialog.qml
│       └── SourceDialog.qml
│
├── tests/
│   ├── __init__.py
│   ├── database_test.py
│   ├── retrieval_tests.py
│   ├── txt_tests.py
│   ├── docx_tests.py
│   ├── pdf_tests.py
│   ├── exporter_tests.py
│   └── test_mail.eml
│
├── experiments/
│   └── ...
│
└── assets/
    └── ...
```

The exact structure is still evolving as the project grows.

---

## Testing

The project contains automated unit tests for several core components.

### Database tests

Database tests cover functionality such as:

- Adding knowledge
- Duplicate handling
- Editing knowledge
- Deleting knowledge
- Searching
- Sorting

### Retrieval tests

Retrieval tests use mocked dependencies where appropriate and cover functionality such as:

- Empty knowledge bases
- Similarity-based sorting
- Similarity threshold filtering
- Top-k limiting

In addition to unit tests, production-oriented evaluation separates retrieval success from generation success. This makes it possible to distinguish between failures to retrieve relevant knowledge and failures where the language model misuses otherwise correct context.

### Document import tests

Automated tests currently cover TXT, DOCX and PDF parsing and import
logic, including invalid files, empty content, source handling,
chunk creation and mocked database/embedding dependencies.

The application has also been tested with heterogeneous benchmark knowledge bases containing approximately 1,200 and 10,000 entries. These tests included repeated entity names across different domains to evaluate both retrieval accuracy and scalability.

---

## Continuous integration

GitHub Actions is used to execute automated tests.

Current coverage includes database, retrieval, TXT, DOCX, PDF and export-related tests.

This helps detect regressions before changes are merged further into the project.

---

## Performance

Performance work currently focuses on:

- Embedding-model startup time
- Semantic-retrieval latency
- Document parsing and embedding time
- Language-model generation time
- Keeping long-running work outside the GUI thread
- Reducing unnecessary model loading
- Evaluating CPU and potential GPU performance

The embedding model is preloaded during application startup.

Language-model generation is performed in a background thread so that question processing does not freeze the QML interface.

Document importing and embedding can still involve blocking work and may be moved to background processing in future development.

### Scalability observations

With approximately 1,200 entries, retrieval averaged around 0.34 seconds per query.

With approximately 10,000 entries, retrieval averaged around 2.7 seconds per query in the tested environment.

The increase was roughly proportional to corpus size, suggesting approximately linear scaling for the current retrieval implementation at these test sizes.

At 10,000 entries, retrieval quality remained strong in the tested question set. Most observed incorrect answers were generation errors rather than failures to retrieve relevant knowledge.

---

## Current quality evaluation

Retrieval and answer quality are still active development areas.

Unexpected answers may originate from several different parts of the RAG pipeline, including:

- Document chunking
- Embedding quality
- Similarity threshold
- Top-k selection
- Retrieved context
- Prompt construction
- Language-model capability

Current evaluation therefore measures retrieval quality separately from language-model answer quality rather than assuming that poor answers are caused by the model alone.

Recent evaluation has shown that retrieval remains reliable even with larger heterogeneous knowledge bases and repeated entity names.

However, observed generation failures include:
- Selecting an attribute from another highly ranked context entry
- Mixing information from similarly named entries
- Producing a value that is not present in the retrieved context
- Reporting insufficient information even when the context supports a simple conclusion

These results suggest that the retrieval pipeline is relatively mature, while generation reliability remains a more significant limitation of the current local model.

---

## Potential future development

Current ideas and areas under consideration include:

### Knowledge and documents

- Drag-and-drop document import
- Opening original source files directly from knowledge entries
- Pagination for large knowledge bases
- Improved PDF parsing
- OCR support for scanned documents
- Additional document formats
- Improved browsing and searching of answer-source knowledge entries

### Chat and context

- Conversation history
- Multiple conversation tabs or sessions
- Persistent conversational context
- Opening the original source from an answer reference

### Configuration

- User-configurable RAG similarity threshold
- User-configurable top-k retrieval value
- Persistent configuration
- Different operating modes
- Interface language selection
- Additional language-model options
- Runtime model selection

### Data management

- JSON backup and restore
- Development/test data for UI work without loading the normal database

### AI integration

- Continued evaluation of local language models
- External LLM providers
- OpenAI-compatible APIs
- Future integration with internal AI systems
- Allowing the application to request information from other agents or information sources when local knowledge is insufficient

### Performance and testing

- Background document embedding/import
- Additional unit tests
- GUI testing
- Larger retrieval-quality benchmarks
- GPU inference
- Additional model benchmarking

These areas are exploratory and may change depending on project requirements and technical constraints.

---

## Integration considerations

Future development may depend on the intended deployment environment.

Important considerations include:

- Whether the application must operate fully offline
- Whether an internal AI or LLM API is available
- Whether external AI providers are permitted
- Which document and knowledge formats are most important
- Expected hardware environments
- Handling of sensitive or classified information
- Deployment and packaging requirements
- Logging and audit requirements
- Third-party licensing requirements

These constraints may influence future architectural decisions.

---

## Language conventions

The project currently uses English for:

- Source code
- Variable and function names
- Docstrings
- Technical documentation
- README documentation

The application interface and user-provided knowledge may currently be written in Swedish.

Support for selectable interface languages may be added later.

---

## Technology

Current technologies and libraries include:

- Python
- PySide6
- QML / Qt Quick
- SQLite
- Sentence Transformers
- Hugging Face Transformers
- PyTorch
- Qwen
- NumPy
- scikit-learn
- python-docx
- pypdf

---

## Project status

Second Brain is currently a working end-to-end prototype under active development.

Core functionality for storing, importing, retrieving and managing knowledge is operational.

The RAG pipeline has now also been evaluated with larger heterogeneous knowledge bases, including a 10,000-entry scalability test.

The current development focus is shifting toward:

- User-interface and usability improvements
- User-configurable RAG settings
- Improved source / knowledge inspection
- Documentation and user guidance
- Data management
- Additional application features and integrations
- Performance improvements where justified by measured bottlenecks
- Final testing and project reflection

---

## Licensing

Current major dependencies include:

- PySide6 / Qt – LGPLv3, GPLv3, or commercial licensing depending on component and usage.
- Sentence Transformers – Apache License 2.0.
- Hugging Face Transformers – Apache License 2.0.
- Qwen3-1.7B – Apache License 2.0.
- PyTorch – BSD-style license; bundled third-party components may use additional licenses.
- NumPy – modified BSD license.
- scikit-learn – BSD 3-Clause license.
- python-docx – MIT License.
- pypdf BSD 3-Clause license.
