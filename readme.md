# Second Brain

Projekt för LIA-perioden 2026-09-28 till 2026-11-20.

## Syfte

Utveckla ett Python-baserat kunskapsverktyg med ett QML-gränssnitt.

Projektets exakta krav, arkitektur och tekniska lösningar kommer
att definieras tillsammans under LIA-perioden.

## Funktioner / Egenskaper

Applikationen ska kunna lagra information i en databas som fungerar som ett slags "second brain". Den lagrade kunskapen ska sedan kunna användas och sökas genom ett chattliknande gränssnitt.

En möjlig lösning är att låta interaktionen ske genom en kedja av:

- Embeddings
- RAG (Retrieval-Augmented Generation)
- LLM (Large Language Model)

Den exakta implementationen bestäms under projektets gång.

## Preliminär teknik

- Python
- PySide6 / QML
- Git / GitHub
- SQLite
- sentence-transformers
- Hugging Face Transformers
- Qwen2.5-3B-Instruct

De exakta biblioteken och tekniska besluten dokumenteras allt eftersom de fattas.

## Struktur

- `main.py` – applikationens startpunkt
- `backend.py` – kommunikation mellan Python och QML
- `database.py` – datalagring
- `qml/` – användargränssnitt

## Status

Projektstruktur skapad inför projektstart.
Implementation påbörjas under LIA-perioden.


## Referenser

### Python
- [Python Documentation](https://docs.python.org/3/)
- [Python Tutorial](https://docs.python.org/3/tutorial/)

### PySide6 / QML
- [Qt for Python / PySide6](https://doc.qt.io/qtforpython-6/)
- [PySide6 Getting Started](https://doc.qt.io/qtforpython-6/quickstart.html)
- [QML Reference](https://doc.qt.io/qt-6/qmlreference.html)
- [QML Tutorial](https://doc.qt.io/qt-6/qml-tutorial.html)
- [Qt Quick](https://doc.qt.io/qt-6/qtquick-index.html)

### Databas
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [SQLite SQL Language](https://sqlite.org/lang.html)

### AI / RAG
- [Sentence Transformers](https://www.sbert.net/)
- [Sentence Transformers Quickstart](https://www.sbert.net/docs/quickstart.html)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers/index)
- [Transformers Quickstart](https://huggingface.co/docs/transformers/quicktour)
- [Qwen2.5-3B-Instruct](https://huggingface.co/Qwen/Qwen2.5-3B-Instruct)