import aiosqlite
from telethon import types


class DB:
    def __init__(self, filename: str):
        self._filename = filename
        self._table_name = "Users"

    async def setup(self):
        async with aiosqlite.connect(self._filename) as db:
            await db.execute(f'CREATE TABLE IF NOT EXISTS {self._table_name} (id, username, full_name)')

    async def get_user_by_id(self, user_id: int):
        async with aiosqlite.connect(self._filename) as db:
            users = list()
            async with db.execute(f"SELECT * FROM {self._table_name} WHERE id = ?", (user_id,)) as cur:
                async for row in cur:
                    users.append(row)
            return users[-1] if len(users) > 0 else None

    async def add_user(self, user: types.User):
        async with aiosqlite.connect(self._filename) as db:
            await db.execute(f"INSERT INTO {self._table_name} (id, username, full_name) VALUES (?,?,?)", (user.id, user.username, user.first_name))
            await db.commit()

    async def get_all_users(self):
        users = list()
        async with aiosqlite.connect(self._filename) as db:
            async with db.execute(f"SELECT * FROM {self._table_name}") as cursor:
                async for row in cursor:
                    users.append(row)
                    # print(row)
        return users
