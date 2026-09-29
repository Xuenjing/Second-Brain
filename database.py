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
    created_at TEXT)
    """)

    connection.commit()
    connection.close()

def add_knowledge(text, source="manual"):
    '''
    Anslut till knowledge.db och lägg till text om den inte redan finns inlagd
    '''
    connection = sqlite3.connect("knowledge.db")
    cursor = connection.cursor()
    created_at = datetime.now().isoformat()
    cursor.execute(
        '''
        INSERT OR IGNORE INTO knowledge (text, source, created_at)
        VALUES (?, ?, ?)
        ''',
        (text, source, created_at)
    )

    connection.commit()
    connection.close()

def get_all_knowledge():
    connection = sqlite3.connect("knowledge.db")
    cursor = connection.cursor()
    cursor.execute("SELECT id, text, source, created_at FROM knowledge")
    rows = cursor.fetchall() # hämta alla rader som matchar select
    connection.close()
    return rows

def add_txt_file_to_database(file_path):
    '''
    Receieve, read and add the contents of a .txt file to the knowledge database,
    unless the file does not exist or is empty
    '''
    path = Path(file_path)
    if not path.exists():
        return False
    if path.suffix.lower() != ".txt":
        return False
    text = path.read_text(encoding="utf-8")

    if not text.strip():
        return False
    add_knowledge(
        text,
        source = path.name
    )
    return True


# testing database methods
if __name__ == "__main__":
    initialize_database()

    add_knowledge("Matsalen öppnar kl 10", source="manual") # add to database

    add_txt_file_to_database("test.txt") # add contents of txt-file to db
    add_txt_file_to_database("test2.txt") # try to an empty .txt-file
    add_txt_file_to_database("test3.txt") # try to add a non-existing .txt-file

    all_knowledge = get_all_knowledge() # get and print entire database
    for row in all_knowledge:
        print(row)