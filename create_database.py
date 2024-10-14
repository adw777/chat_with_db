import sqlite3

# Function to create the database and sample data
def create_sample_database():
    conn = sqlite3.connect('music_database.db')
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS singer (
        Singer_ID INTEGER PRIMARY KEY,
        Name TEXT,
        Country TEXT,
        Song_Name TEXT,
        Song_release_year TEXT,
        Age INTEGER,
        Is_male BOOLEAN
    )
    ''')

    # Insert sample data
    sample_data = [
        (1, 'John Doe', 'USA', 'American Song', '2020', 35, True),
        (2, 'Jane Smith', 'France', 'French Melody', '2019', 28, False),
        (3, 'Pierre Dupont', 'France', 'Chanson d\'amour', '2021', 45, True),
        (4, 'Marie Claire', 'France', 'La vie en rose', '2018', 32, False),
    ]

    cursor.executemany('INSERT INTO singer VALUES (?, ?, ?, ?, ?, ?, ?)', sample_data)
    conn.commit()
    conn.close()
