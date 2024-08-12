"""
Database protocols.
"""
from typing import Protocol, AsyncContextManager

from sqlalchemy.ext.asyncio import AsyncSession


class SQLAlchemyDatabaseProtocol(Protocol):
    """
    SQLAlchemy database protocol.
    """
    def session(self) -> AsyncContextManager[AsyncSession]:
        """
        Implements method that returns SQLAlchemy session context manager.
        """
        ...

    def init(self):
        """
        Implements initialization.
        """
        ...
