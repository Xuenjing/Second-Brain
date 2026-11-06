"""
Database layer for the Second Brain knowledge base.

This module handles initialization, storage, retrieval, editing,
deletion and searching of knowledge entries stored in SQLite.
Embeddings are serialized as JSON before being stored in the database.
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path

import numpy as np

DATABASE_PATH = "knowledge.db"

def initialize_database() -> None:
    """
    Create the SQLite knowledge database unless already created.
    """

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
    """Add a knowledge entry to the database.
    Embedding is converted from NumPy array to JSON before storage.
    Duplicate entries are ignored.

    Args:
        text: Knowledge text to store.
        embedding: Embedding vector associated with the text.
        source: Source of the entry (manually or from a file).
    
    Returns: 
        True if an entry was added, otherwise False.
    """

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    created_at = datetime.now().isoformat()

    # Convert the NumPy embedding to a JSON string for database storage
    embedding_json = json.dumps(embedding.tolist()) 
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
    """Get all entries from the database.
    Converts embedding JSON back into a Python list.

    Args:
        sort_order: Sort order by creation time (ascending or descending)

    Returns:
        A list containing dictionaries of all knowledge entries.
    """

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
    rows = cursor.fetchall()
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


def get_knowledge_by_id(knowledge_id: int) -> dict | None:
    """Return a knowledge entry by database ID.
    
        Args:
            knowledge_id: Database ID of an entry post.

        Returns:
            A dictionary of the knowledge entry if it exists, otherwise None.
    """

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM knowledge WHERE id = ?",
        (knowledge_id,)
    )

    row = cursor.fetchone()
    connection.close()

    return dict(row) if row else None


def get_knowledge_sources(sort_order: str = "desc") -> list[dict]:
    """
    Retrun all unique sources together with
    the number of entries belonging to each source.

    Args:
        sort_order: Sort sources by their newest or oldest entry.
    
    Returns:
        A list of dictionaries containing the source name,
        entry count and creation time.
    """

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    if sort_order == "asc":
        order = "ASC"
    else:
        order = "DESC"

    cursor.execute(f"""
        SELECT
            source,
            COUNT(*) AS entry_count,
            MIN(created_at) AS source_date
        FROM knowledge
        GROUP BY source
        ORDER BY source_date {order}
    """)

    rows = cursor.fetchall()
    connection.close()

    sources = []

    for source, entry_count, source_date in rows:
        sources.append({
            "source": source,
            "entry_count": entry_count,
            "source_date": source_date,
        })

    return sources
    

def delete_knowledge(knowledge_id: int) -> bool:
    """Delete a knowledge entry from the database.

    Args:
        knowledge_id: Database ID for the entry to delete.
    
    Returns:
        True if an entry was deleted, False if not.
    """
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM knowledge WHERE id = ?", (knowledge_id,))

    # true if something was removed, false if not
    deleted = cursor.rowcount > 0

    connection.commit()
    connection.close()
    return deleted


def delete_knowledge_by_source(source: str) -> int:
    """Delete all knowledge entries corresponding to the same source.
    
    Args:
        source: Source name whose entries to be deleted.
    
    Returns:
        Number of deleted knowledge entries.
    """

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM knowledge WHERE source = ?",
        (source,)
    )

    deleted_count = cursor.rowcount

    connection.commit()
    connection.close()

    return deleted_count


def edit_knowledge(knowledge_id: int, new_text: str, new_embedding: np.ndarray) -> bool:
    """Update the text and embedding of an existing knowledge entry.

    Args:
        knowledge_id: Database ID of the entry to update.
        new_text: Replacement text for the entry.
        new_embedding: Embedding vector for the updated text.

    Returns:
        True if an entry was updated, False if not.
    """
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
    """Search stored knowledge by text or source.
    
    Args:
        search_term: Search term to match against text and source. 

    Returns:
        A list of dictionaries containing matched knowledge entries.
    """
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

    sources = get_knowledge_sources()

    for source in sources:
        print(source)

