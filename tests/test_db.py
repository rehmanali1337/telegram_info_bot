import pytest
from app.db import DB


@pytest.fixture
async def db():
    db = DB("test.db")
    await db.setup()
    return db


@pytest.mark.asyncio
async def test_create_table(db: DB):
    pass
    # print(db)


@pytest.mark.asyncio
async def test_get_all_users(db: DB):
    users = await db.get_all_users()
    print(users)
