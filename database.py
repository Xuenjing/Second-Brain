"""
Database layer for the Second Brain knowledge base.

This module handles initialization, storage, retrieval, editing,
deletion and searching of knowledge entries stored in SQLite.
Embeddings are serialized as JSON before being stored in the database.
"""

import sqlite3
from datetime import datetime
from pathlib import Path
import json
import numpy as np

DATABASE_PATH = "knowledge.db"

def initialize_database() -> None:
    '''
    Creates the SQLite knowledge database unless already created.
    '''
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS knowledge (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL UNIQUE,
    source TEXT,
    created_at TEXT,
    embedding TEXT)
    """)

    connection.commit()
    connection.close()

def add_knowledge(text: str, embedding: np.ndarray, source: str = "manual") -> bool:
    '''
    Add a knowledge entry to the database.
    Embedding is converted from NumPy array to JSON before storage.
    Duplicate entries are ignored.
    Returns True if entry was added, False if not.
    '''
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    created_at = datetime.now().isoformat()
    embedding_json = json.dumps(embedding.tolist()) # convert the NumPy embedding to a JSON string for database storage
    cursor.execute(
        '''
        INSERT OR IGNORE INTO knowledge (text, source, created_at, embedding)
        VALUES (?, ?, ?, ?)
        ''',
        (text, source, created_at, embedding_json)
    )

    added = cursor.rowcount > 0

    connection.commit()
    connection.close()

    return added

def get_all_knowledge(sort_order: str = "desc") -> list[dict]:
    '''
    Get all entries from the database.
    Converts embedding JSON back into a python list.
    Returns a list of dictionaries containing the stored entries.
    '''
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    if sort_order == "asc":
        order = "asc"
    else:
        order = "desc"

    cursor.execute(f"""
        SELECT id, text, source, created_at, embedding
        FROM knowledge
        ORDER BY created_at {order}
        """)
    rows = cursor.fetchall() # fetch all rows matching select
    connection.close()
    
    knowledge = []
    for row_id, text, source, created_at, embedding_json in rows:
        embedding = json.loads(embedding_json) # converts JSON format back into a python list
        knowledge.append({
            "id": row_id,
            "text": text,
            "source": source,
            "created_at": created_at,
            "embedding": embedding
        })

    return knowledge

# NOT CURRENTLY IN USE: FLAGGED FOR REMOVAL ???
def add_txt_file_to_database(file_path, model):
    '''
    Receieve, read and add the contents of a .txt file to the knowledge database,
    unless the file does not exist or is empty.
    Creates an embedding before storing.
    '''
    path = Path(file_path)
    if not path.exists():
        return False
    if path.suffix.lower() != ".txt":
        return False
    text = path.read_text(encoding="utf-8")

    if not text.strip():
        return False

    embedding = model.encode(text)
    
    add_knowledge(
        text,
        embedding,
        source = path.name
    )
    return True

def delete_knowledge(knowledge_id: int) -> bool:
    '''
    Delete a knowledge entry from the database.
    Returns True if an entry was deleted, False if not.
    '''
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM knowledge WHERE id = ?", (knowledge_id,))

    # true if something was removed, false if not
    deleted = cursor.rowcount > 0

    connection.commit()
    connection.close()
    return deleted

def edit_knowledge(knowledge_id: int, new_text: str, new_embedding: np.ndarray) -> bool:
    '''
    Update the text and embedding of an existing knowledge entry.
    New embedding is converted from NumPy array to JSON before storage.
    Returns True if an entry was updated, False if not.
    '''
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        # Commit on success and roll back if an error occurs.
        with connection:
            cursor = connection.cursor()
            embedding_json = json.dumps(new_embedding.tolist())
            cursor.execute("""
            UPDATE knowledge
            SET text = ?, embedding = ?
            WHERE id = ?
            
            """, (new_text, embedding_json, knowledge_id))

            # true if updated, false if not
            return cursor.rowcount > 0
    finally:
        connection.close()

def search_knowledge(search_term: str) -> list[dict]:
    '''
    Search stored knowledge by text or source.
    Returns a list of dictionaries containing matched knowledge entries.
    '''
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
    SELECT id, text, source, created_at
    FROM knowledge
    WHERE text LIKE ? OR source LIKE ?
    """, (f"%{search_term}%", f"%{search_term}%"))

    rows = cursor.fetchall()
    connection.close()

    results = []

    for row_id, text, source, created_at in rows:

        results.append({
            "id": row_id,
            "text": text,
            "source": source,
            "created_at": created_at
        })

    return results


# testing database methods
if __name__ == "__main__":

    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    text = "The school opens at 8.00AM."
    embedding = model.encode(text)

    initialize_database()

    add_knowledge(text, embedding, source="manual") # add to database

    # add contents of txt-file to db(1), try to add an empty file (2), and a non-existing file (3)
    add_txt_file_to_database("test.txt", model)
    add_txt_file_to_database("test2.txt", model)
    add_txt_file_to_database("test3.txt", model)

    all_knowledge = get_all_knowledge() # get entire database

    # print it
    for row in all_knowledge:
        print({
            "id": row["id"],
            "text": row["text"],
            "source": row["source"],
            "created_at": row["created_at"],
            "embedding_length": len(row["embedding"])
        })

