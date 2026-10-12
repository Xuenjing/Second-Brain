# Second Brain

Second Brain is a desktop application designed to provide a local knowledge base where users can store information and later retrieve it through natural-language questions.

The application combines local knowledge storage, semantic search, retrieval and language models to provide answers based on information stored in the knowledge base.

## Current functionality

The current prototype supports:

- Manual knowledge input through the user interface
- Import of `.txt` files
- Local storage using SQLite
- Storage of source information and creation timestamps
- Embedding generation for stored knowledge
- Semantic retrieval using cosine similarity
- Retrieval-Augmented Generation (RAG)
- Local language model integration
- Knowledge base viewer
- Search within the knowledge base
- Editing stored knowledge
- Deleting stored knowledge
- Sorting knowledge by creation date
- Duplicate handling for stored knowledge
- System tray support
- Communication between QML and Python using Qt signals and slots
- Unit tests for database and retrieval functionality
- Benchmark scripts for retrieval thresholds, embedding models and local language models

## Architecture

The application currently consists of several main parts.

### User interface

The user interface is built with QML and Qt Quick.

QML communicates with the Python backend through PySide6 using signals and slots.

### Backend

The Python backend handles communication between the user interface and the underlying application logic.

Its responsibilities currently include:

- Receiving user questions
- Adding knowledge manually
- Importing text files
- Loading knowledge for the user interface
- Searching, editing, deleting and sorting stored knowledge
- Performing semantic retrieval
- Sending retrieved context to the language model
- Returning generated answers to the user interface

### Knowledge storage

SQLite is currently used as the local knowledge database.

Knowledge entries can contain:

- Text
- Source
- Creation timestamp
- Embedding

Duplicate text entries are prevented by the database.

The database is initialized when the backend starts to ensure that the required schema exists before the application attempts to access stored knowledge.

### Embeddings and retrieval

Embeddings are currently generated using:

`sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`

The user's question is converted into an embedding and compared with stored knowledge using cosine similarity.

Relevant entries are selected using a similarity threshold and top-k retrieval.

The current similarity threshold is:

`0.45`

This value was selected after benchmarking several thresholds against a 200-entry test dataset and a set of representative retrieval questions.

Alternative embedding models have also been evaluated. In particular:

`intfloat/multilingual-e5-small`

showed improved ranking for several difficult retrieval queries while maintaining similar runtime performance. However, its similarity-score distribution differs significantly from the current MiniLM model, so additional filtering and threshold evaluation is required before replacing the current embedding model.

### Language model

The current local language model is:

`Qwen/Qwen3-1.7B`

The model was selected after benchmarking:

- `Qwen/Qwen3-0.6B`
- `Qwen/Qwen3-1.7B`
- `Qwen/Qwen3-4B-Instruct-2507`

Qwen3-0.6B provided the fastest generation but showed quality issues on some multi-fact and ranking questions.

Qwen3-4B provided good answer quality but required significantly more generation time.

Qwen3-1.7B provided the best balance between answer quality and CPU performance and is therefore currently used as the default local model.

The language model is accessed through a separate provider class rather than directly from the rest of the application.

This is intended to make it possible to replace the current local model with another local model, an external provider or an internal AI solution in the future.

Qwen thinking mode is explicitly disabled through the model's chat template to avoid generating unnecessary reasoning output.

## Current project structure

The project currently contains components such as:

```text
Second-Brain---LIA-PROJECT/
│
├── main.py
├── backend.py
├── database.py
├── retrieval.py
├── performance.py
│
├── llm/
│   ├── __init__.py
│   └── local_provider.py
│
├── qml/
│   └── main.qml
│
├── tests/
│   ├── database_test.py
│   ├── retrieval_test.py
│   ├── retrieval_threshold_test.py
│   ├── retrieval_model_benchmark.py
│   └── llm_model_benchmark.py
│
└── README.md
```

The structure is still under development and may change as the project grows.

## Testing and evaluation

The project currently contains automated unit tests for core database and retrieval functionality.

Database tests cover functionality such as:

- Adding knowledge
- Duplicate handling
- Deleting entries
- Editing entries
- Searching
- Sorting

Retrieval tests use mocked dependencies to test:

- Empty knowledge bases
- Similarity-based sorting
- Similarity threshold filtering
- Top-k limiting

Separate benchmark scripts are used to evaluate:

- Similarity thresholds
- Local language models
- Embedding models
- Retrieval quality on larger datasets

A generated dataset containing 200 knowledge entries and 25 representative questions is currently used for retrieval evaluation.

## Performance

Performance measurements show that model loading and language-model inference account for most of the application's execution time.

On the current development environment, cached model startup is significantly faster than earlier tests with larger models.

Recent observations include:

- Semantic retrieval typically completes in a small fraction of a second
- Embedding 200 knowledge entries takes approximately half a second with the currently evaluated small embedding models
- Qwen3-1.7B provides significantly faster response generation than Qwen3-4B while maintaining similar answer quality in the current benchmark
- QML loading itself remains comparatively fast

Performance work is still ongoing.

Areas being considered include:

- Moving long-running AI operations away from the GUI thread
- Background or asynchronous embedding generation
- Progress or loading indicators
- GPU inference
- External AI providers
- Further model-loading optimization

## Planned development

Current areas being considered for further development include:

- Automated unit testing through GitHub Actions
- Improved type hints and docstrings
- More consistent language conventions across the codebase
- Moving LLM generation away from the GUI thread
- Background or asynchronous embedding and retrieval work
- Loading and progress feedback for long-running operations
- External LLM provider support
- Investigation of OpenAI-compatible APIs
- Future integration with an internal AI solution
- Import of additional knowledge formats
- Email import
- PDF import
- Word document import
- Investigation of drag-and-drop document import
- GUI testing using tools such as Squish
- Continued evaluation of retrieval models and filtering strategies
- GPU support and performance testing
- Optional interface language switching
- Voice input

Some of these areas are currently exploratory and may change depending on project requirements or specific constraints.

## Integration considerations

Future development may depend on requirements specific to the intended environment.

Areas requiring further clarification include:

- Whether the application must operate fully offline
- Whether an internal AI or LLM API is available
- Whether external AI providers are permitted
- Which document and knowledge formats are most relevant
- Expected hardware environments
- Requirements for handling sensitive or classified information
- Deployment and packaging requirements
- Logging and audit requirements
- Licensing and third-party dependency restrictions

These questions will help guide future architectural decisions.

## Language conventions

The project uses English for:

- Source code
- Variable and function names
- Technical documentation
- README documentation

The application interface and user-provided knowledge may be written in Swedish.

Support for switching interface language may be investigated later.

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

## Documentation

Official documentation used during development includes:

- Python documentation
- PySide6 documentation
- Qt / QML documentation
- SQLite documentation
- Sentence Transformers documentation
- Hugging Face Transformers documentation
- PyTorch documentation

## Project status

The project is currently in active development.

A working end-to-end prototype currently supports the following flow:

```text
User question
      ↓
QML interface
      ↓
Python backend
      ↓
Semantic retrieval
      ↓
Relevant knowledge
      ↓
Language model
      ↓
Generated answer
      ↓
QML interface
```

The  current work focuses increasingly on testing, performance, retrieval quality, asynchronous processing and future integration options.

## Licensing

Main dependencies include:

- PySide6 / Qt – LGPLv3, GPLv3, or commercial licensing depending on component and usage.
- Sentence Transformers – Apache License 2.0.
- Hugging Face Transformers – Apache License 2.0.
- Qwen3-1.7B – Apache License 2.0.
- PyTorch – BSD-style license; bundled third-party components may use additional licenses.
- NumPy – modified BSD license.
- scikit-learn – BSD 3-Clause license.