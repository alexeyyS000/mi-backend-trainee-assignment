"""
Worker DI container.
"""
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.wiring import providers
from redis.client import Redis

from services.amount_ads_observer.dal import AdsObserversRepository, AdsObserversStatRepository
from services.db import AsyncDatabase
from services.db.config import async_database_settings
from services.private_avito_api_executor.grpc.client import PrivateAvitoApiExecutorGrpcClient
from services.redis.config import REDIS_HOST, REDIS_PORT
from services.worker.config import worker_settings


class WorkerContainer(DeclarativeContainer):
    redis_client = providers.Singleton(
        Redis,
        host=REDIS_HOST,
        port=REDIS_PORT
    )

    private_avito_api_executor_client = providers.Singleton(
        PrivateAvitoApiExecutorGrpcClient,
        worker_settings.private_avito_api_executor_grpc_server_addr
    )

    db = providers.Singleton(AsyncDatabase, db_url=async_database_settings.db_url)
    ads_observers_repository = providers.Factory(
        AdsObserversRepository,
        session_factory=db.provided.session
    )
    ads_observers_stats_repository = providers.Factory(
        AdsObserversStatRepository,
        session_factory=db.provided.session
    )
