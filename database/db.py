import sqlite3

def save_hand(hero_stack_bb, pot_size, villain_bet, decision, notes):
    conn = sqlite3.connect("poker_review.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO hands (hero_stack_bb, pot_size, villain_bet, decision_hero, notes)
    VALUES (?, ?, ?, ?, ?)
    """, (hero_stack_bb, pot_size, villain_bet, decision, notes))

    conn.commit()
    conn.close()


def get_hands():
    conn = sqlite3.connect("poker_review.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM hands")
    rows = cursor.fetchall()

    conn.close()
    return rows