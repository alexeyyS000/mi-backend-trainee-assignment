"""
Database service.
"""
from contextlib import asynccontextmanager

from loguru import logger
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool

from utils.sqlalchemy.protocols import SQLAlchemyDatabaseProtocol

Base = declarative_base()


class AsyncDatabase(SQLAlchemyDatabaseProtocol):
    def __init__(self, db_url: str):
        """
        :param db_url: Database URL.
        """
        self._engine = create_async_engine(
            db_url,
            echo=True,
            poolclass=NullPool
        )
        self._session_factory = sessionmaker(
            self._engine,
            expire_on_commit=False,
            class_=AsyncSession
        )

    @asynccontextmanager
    async def session(self):
        session: AsyncSession = self._session_factory()
        try:
            yield session
        except Exception as err:
            logger.error(f'Session rollback because of exception: {err}')
            await session.rollback()
        finally:
            await session.close()

    async def init(self):
        """
        Database initialization.
        """
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)


# TODO: make implementation through protocol
# class Database:
#     def __init__(self, db_url: str) -> None:
#         """
#         :param db_url: Database URL.
#         """
#         self._engine = create_engine(db_url, echo=True)
#         self._session_factory = sessionmaker(
#             self._engine,
#             expire_on_commit=False,
#             class_=Session
#         )
#
#     @contextmanager
#     def session(self) -> Callable[..., AbstractContextManager[Session]]:
#         session: Session = self._session_factory()
#         try:
#             yield session
#         except Exception:
#             logger.exception("Session rollback because of exception")
#             session.rollback()
#             raise
#         finally:
#             session.close()
#
#     def init(self):
#         """
#         Database initialization.
#         """
#         Base.metadata.create_all(self._engine)
