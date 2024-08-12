"""
Announcement observer DI container.
"""
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.wiring import providers

from services.amount_ads_observer.dal import AdsObserversRepository, AdsObserversStatRepository
from services.db import AsyncDatabase
from services.db.config import async_database_settings


class AmountAdsObserverContainer(DeclarativeContainer):
    db = providers.Singleton(
        AsyncDatabase,
        db_url=async_database_settings.db_url
    )
    ads_observers_repository = providers.Factory(
        AdsObserversRepository,
        session_factory=db.provided.session
    )
    ads_observers_stats_repository = providers.Factory(
        AdsObserversStatRepository,
        session_factory=db.provided.session
    )
