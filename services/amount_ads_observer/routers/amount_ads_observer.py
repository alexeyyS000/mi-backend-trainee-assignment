from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from services.amount_ads_observer.container import AmountAdsObserverContainer
from services.amount_ads_observer.dal import AdsObserversRepository, AdsObserversStatRepository
from services.amount_ads_observer.schemas.ads_observer import AdsObserverCreate, AdsObserver
from services.amount_ads_observer.schemas.ads_observer_stat import AdsObserverStat
from services.worker.app import save_curr_ads_amount


router = APIRouter(prefix='/ads/amount/observer')


@router.get('/stat', response_model=List[AdsObserverStat])
@inject
async def get_stat(
        ads_observer_id: int = Query(),
        from_: int = Query(),
        to: int = Query(),
        ads_observers_stats_repository: AdsObserversStatRepository = Depends(
            Provide[AmountAdsObserverContainer.ads_observers_stats_repository]
        )
):
    return await ads_observers_stats_repository.select_interval(ads_observer_id, from_, to)


@router.post('/add', response_model=AdsObserver)
@inject
async def add_observation(
        ads_observer_data: AdsObserverCreate,
        ads_observers_repo: AdsObserversRepository = Depends(
            Provide[AmountAdsObserverContainer.ads_observers_repository]
        )
):
    ads_observer = await ads_observers_repo.add_one(ads_observer_data)
    save_curr_ads_amount.delay(
        ads_observer_id=ads_observer.id,
        location_id=ads_observer.location_id,
        query=ads_observer.query
    )
    return ads_observer
