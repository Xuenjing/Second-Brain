# Second Brain

Second Brain is a desktop application with the purpose to provide a local knowledge base where users can store information and later retrieve it through natural-language questions.

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
- Duplicate handling for stored knowledge
- System tray support
- Communication between QML and Python using Qt signals and slots

## Architecture

The application currently consists of several main parts:

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
- Performing retrieval
- Sending context to the language model
- Returning generated answers to the user interface

### Knowledge storage

SQLite is currently used as the local knowledge database.

Knowledge entries can contain:

- Text
- Source
- Creation timestamp
- Embedding

Duplicate text entries are prevented by the database.

### Embeddings and retrieval

Embeddings are currently generated using:

`paraphrase-multilingual-MiniLM-L12-v2`

The user's question is converted into an embedding and compared with stored knowledge using cosine similarity.

Relevant entries are selected using a similarity threshold and top-k retrieval.

The retrieved entries are then used as context for the language model.

### Language model

The current local language model is:

`Qwen/Qwen3-4B-Instruct-2507`

The language model is accessed through a separate provider class rather than directly from the rest of the application.

This is intended to make it possible to replace the current local model with another local model, an external provider or an internal Saab AI solution in the future.

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
└── README.md
```

The structure is still under development and may change as the project grows.

## Performance

Initial performance measurements have shown that model loading and local language-model inference currently account for most of the application's startup and response time.

Recent measurements showed approximately:

- Backend import and embedding-related initialization: ~28 seconds
- Local LLM initialization: ~20 seconds
- QML loading: <1 second
- Total application startup: ~50 seconds

Retrieval itself is currently significantly faster than local LLM generation.

Further work will investigate:

- Smaller or faster local language models
- GPU inference
- External AI providers
- Model-loading performance

## Planned development

Current areas being considered for further development include:

- Search within the knowledge base
- Editing stored knowledge
- Deleting stored knowledge
- Sorting knowledge by date
- Testing retrieval with larger datasets
- Evaluation of similarity threshold and top-k values
- External LLM provider support
- GPU support and performance testing
- Unit and integration testing
- Improved project structure
- License documentation
- Email import
- Voice input
- Optional language switching

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

## Documentation

Official documentation used during development:

- Python documentation
- PySide6 documentation
- Qt / QML documentation
- SQLite documentation
- Sentence Transformers documentation
- Hugging Face Transformers documentation
- PyTorch documentation

## Project status

The project is currently in active development.

A first end-to-end prototype is working, including:

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

The next phase of development focuses on improving knowledge management, retrieval quality, model performance and provider flexibility.

## Licensing

Main dependencies include:

- PySide6 / Qt – LGPLv3, GPLv3, or commercial licensing depending on component and usage.
- Sentence Transformers – Apache License 2.0.
- Hugging Face Transformers – Apache License 2.0.
- Qwen3-0.6B – Apache License 2.0.
- PyTorch – BSD-style license; bundled third-party components may use additional licenses.
- NumPy – modified BSD license.
- scikit-learn – BSD 3-Clause license.