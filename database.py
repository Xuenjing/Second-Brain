"""
Databaslager för kunskapsbasen.

Tänkt ansvar:
- lagra kunskap
- läsa lagrad kunskap
- eventuellt lagra embeddings

Databaslösning och schema bestäms tillsammans under projektet.
"""

import sqlite3
from datetime import datetime
from pathlib import Path
import json

DATABASE_PATH = "knowledge.db"

def initialize_database():
    '''
    Skapar kunskapsdatabasen om den inte redan är skapad
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

def add_knowledge(text, embedding, source="manual"):
    '''
    Connect to knowledge.db och add a post if it is not already inserted
    Converts the embedding to json-format
    Returns true if rows were added, false if not
    '''
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    created_at = datetime.now().isoformat()
    embedding_json = json.dumps(embedding.tolist()) # convert embedding to json
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

def get_all_knowledge(sort_order="desc"):
    '''
    Get all posts from knowledge.db as a dictionary
    Converts embedding JSON back into a python list
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

def delete_knowledge(knowledge_id) -> bool:
    '''
    Delete a knowledge post from the database
    '''
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM knowledge WHERE id = ?", (knowledge_id,))

    # true if something was removed, false if not
    deleted = cursor.rowcount > 0

    connection.commit()
    connection.close()
    return deleted

def edit_knowledge(knowledge_id, new_text, new_embedding) -> bool:
    '''
    Updates knowledge posts by receiving new text and new embedding
    from backend, and then making the NumPy array into a python list,
    and then to a JSON string
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

def search_knowledge(search_term) -> list:
    '''
    Returns all knowledge entries that match the search term
    in either the text or source fields.
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

