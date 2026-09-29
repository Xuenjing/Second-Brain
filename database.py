"""
Databaslager för kunskapsbasen.

Tänkt ansvar:
- lagra kunskap
- läsa lagrad kunskap
- eventuellt lagra embeddings

Databaslösning och schema bestäms tillsammans under projektet.
"""

import sqlite3

def initialize_database():
    '''
    Skapar kunskapsdatabasen om den inte redan är skapad
    '''
    connection = sqlite3.connect("knowledge.db")
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS knowledge (
    id INTEGER PRIMARY KEY NOT NULL,
    text TEXT NOT NULL UNIQUE)
    """)

    connection.commit()
    connection.close()

def add_knowledge(text):
    '''
    Anslut till knowledge.db och lägg till text om den inte redan finns inlagd
    '''
    connection = sqlite3.connect("knowledge.db")
    cursor = connection.cursor()
    cursor.execute(
        'INSERT OR IGNORE INTO knowledge (text) values (?)', # ? är placeholder för värdet som skickas i (text,)
        (text,)
    )

    connection.commit()
    connection.close()

def get_all_knowledge():
    connection = sqlite3.connect("knowledge.db")
    cursor = connection.cursor()
    cursor.execute("SELECT id, text FROM knowledge")
    rows = cursor.fetchall() # hämta alla rader som matchar select
    connection.close()
    return rows


# test av databasfunktioner
if __name__ == "__main__":
    initialize_database()

    add_knowledge("Matsalen öppnar kl 10") # lägg till databasen

    all_knowledge = get_all_knowledge() # hämta och skriv ut hela databasen
    for row in all_knowledge:
        print(row)