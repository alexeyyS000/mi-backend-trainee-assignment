"""
Data access layer.
"""
from abc import ABC
from typing import Callable, AsyncContextManager

from sqlalchemy.ext.asyncio import AsyncSession

from utils.common.patterns import Repository


class SQLAlchemyRepository(Repository, ABC):
    """
    SQLAlchemy repository.
    """

    def __init__(self, session_factory: Callable[..., AsyncContextManager[AsyncSession]]):
        self.session_factory: Callable[..., AsyncContextManager[AsyncSession]] = \
            session_factory
