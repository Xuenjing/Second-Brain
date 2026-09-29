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


# test av databasfunktioner
if __name__ == "__main__":
    initialize_database()

    add_knowledge("Matsalen öppnar kl 10", source="manual") # lägg till databasen

    all_knowledge = get_all_knowledge() # hämta och skriv ut hela databasen
    for row in all_knowledge:
        print(row)