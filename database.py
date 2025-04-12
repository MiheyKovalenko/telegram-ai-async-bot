import sqlite3
import json
import aiosqlite

def create_table(table_name, columns):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    columns_str = ', '.join(columns)
    query = f'CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})'
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()


DB_NAME = "bot.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            firstname TEXT,
            lastname TEXT,
            requests INTEGER DEFAULT 0
        )''')
        await db.commit()

async def update_user(user_id, username, firstname, lastname):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users WHERE id=?", (user_id,)) as cursor:
            user = await cursor.fetchone()
        if user:
            await db.execute("UPDATE users SET username=?, firstname=?, lastname=? WHERE id=?",
                             (username, firstname, lastname, user_id))
        else:
            await db.execute("INSERT INTO users (id, username, firstname, lastname) VALUES (?, ?, ?, ?)",
                             (user_id, username, firstname, lastname))
        await db.commit()

async def increment_requests(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("UPDATE users SET requests = requests + 1 WHERE id=?", (user_id,))
        await db.commit()
import json

def init_history_table():
    create_table('history', ['user_id INTEGER PRIMARY KEY', 'messages TEXT'])

def get_user_history(user_id):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute("SELECT messages FROM history WHERE user_id=?", (user_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row:
        try:
            return json.loads(row[0])
        except:
            return []
    return []

def save_user_history(user_id, messages):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    json_data = json.dumps(messages[-20:])
    cursor.execute("REPLACE INTO history (user_id, messages) VALUES (?, ?)", (user_id, json_data))
    conn.commit()
    cursor.close()
    conn.close()
