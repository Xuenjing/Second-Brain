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

def initialize_database():
    '''
    Skapar kunskapsdatabasen om den inte redan är skapad
    '''
    connection = sqlite3.connect("knowledge.db")
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
    Anslut till knowledge.db och lägg till text om den inte redan finns inlagd
    '''
    connection = sqlite3.connect("knowledge.db")
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

    connection.commit()
    connection.close()

def get_all_knowledge():
    '''
    Get all posts from knowledge.db as a dictionary
    Converts embedding JSON back into a python list
    '''
    connection = sqlite3.connect("knowledge.db")
    cursor = connection.cursor()
    cursor.execute("""
        SELECT id, text, source, created_at, embedding
        FROM knowledge
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