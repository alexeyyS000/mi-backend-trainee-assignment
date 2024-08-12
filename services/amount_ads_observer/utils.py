"""
Announcement observer utils.
"""
from services.db import AsyncDatabase


async def async_init_db(db: AsyncDatabase):
    """
    Init database.
    :param db: Database
    """

    await db.init()
