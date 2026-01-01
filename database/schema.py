import sqlite3

def create_database():
    conn = sqlite3.connect("poker_review.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS hands (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        game_type TEXT,
        hero_stack_bb REAL,
        pot_size REAL,
        villain_bet REAL,
        decision_hero TEXT,
        notes TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS analysis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hand_id INTEGER,
        pot_odds REAL,
        estimated_equity REAL,
        recommendation TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(hand_id) REFERENCES hands(id)
    );
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    print("Banco criado com sucesso!")
