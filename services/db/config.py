"""
Database configuration.
"""
from pydantic import BaseSettings


class BaseDatabaseSettings(BaseSettings):
    db_user: str = 'postgres'
    db_password: str = ''
    db_name: str = ''
    db_host: str = 'localhost'
    db_scheme: str = ''

    @property
    def db_url(self):
        return f'{self.db_scheme}://{self.db_user}:{self.db_password}@{self.db_host}/{self.db_name}'


class AsyncDatabaseSettings(BaseDatabaseSettings):
    db_scheme: str = 'postgresql+asyncpg'


class SyncDatabaseSettings(BaseDatabaseSettings):
    db_scheme: str = 'postgresql+psycopg2'


async_database_settings = AsyncDatabaseSettings()
sync_database_settings = SyncDatabaseSettings()
