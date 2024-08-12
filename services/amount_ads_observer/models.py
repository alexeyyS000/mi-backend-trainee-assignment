"""
Announcement observer database models.
"""
from sqlalchemy import Column, Integer, String, ForeignKey

from services.db import Base


class AdsObserver(Base):
    __tablename__ = 'ads_observers'

    id: int = Column(Integer, primary_key=True)
    location_id: int = Column(Integer, nullable=False)
    query: str = Column(String, nullable=False)


class AdsObserverStat(Base):
    __tablename__ = 'ads_observer_stats'

    id: int = Column(Integer, primary_key=True)
    ads_observer_id: int = Column(Integer, ForeignKey('ads_observers.id'), nullable=False)
    timestamp: int = Column(Integer, nullable=False)
    amount: int = Column(Integer, nullable=False)
