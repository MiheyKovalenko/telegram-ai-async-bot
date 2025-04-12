import aiosqlite

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
