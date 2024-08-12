"""
Announcement observer Data Access Layer.
"""
from http import HTTPStatus
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy import select

from services.amount_ads_observer.models import AdsObserver, AdsObserverStat
from services.amount_ads_observer.schemas.ads_observer import AdsObserverCreate
from services.amount_ads_observer.schemas.ads_observer_stat import AdsObserverStatCreate
from utils.sqlalchemy.dal import SQLAlchemyRepository


class AdsObserversRepository(SQLAlchemyRepository):
    """
    Advert observers repository that uses SQLAlchemy.
    """
    async def add_one(self, ads_observer_data: AdsObserverCreate) -> AdsObserver:
        async with self.session_factory() as session:
            async with session.begin():
                ad_observer = AdsObserver(**ads_observer_data.dict())
                session.add(ad_observer)
                await session.commit()
                return ad_observer

    async def get_by_id(self, ads_observer_id: int) -> Optional[AdsObserver]:
        async with self.session_factory() as session:
            stmt = select(AdsObserver).filter_by(id=ads_observer_id)
            res = await session.execute(stmt)
            return res.scalar_one_or_none()


class AdsObserversStatRepository(SQLAlchemyRepository):
    """
    Advert observers statistic repository that uses SQLAlchemy.
    """
    async def add_one(self, ads_observer_data: AdsObserverStatCreate) -> AdsObserverStat:
        async with self.session_factory() as session:
            async with session.begin():
                ad_observer_stat = AdsObserverStat(**ads_observer_data.dict())
                session.add(ad_observer_stat)
                await session.commit()
                return ad_observer_stat

    async def select_interval(self, ads_observer_id: int, from_: int, to: int) -> List[AdsObserverStat]:
        """
        Returns Advert observers statistic records from timestamp interval.

        :param ads_observer_id: Adverts observer ID
        :param from_: Interval begin
        :param to: Interval end
        :return: Advert observers statistic records
        """
        if from_ > to:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='"from" must be less "to"'
            )

        async with self.session_factory() as session:
            stmt = select(AdsObserverStat)\
                    .filter_by(ads_observer_id=ads_observer_id)\
                    .where(AdsObserverStat.timestamp >= from_)\
                    .where(AdsObserverStat.timestamp <= to)
            res = await session.execute(stmt)
            return res.scalars().all()
