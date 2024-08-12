from datetime import datetime, timedelta

from asgiref.sync import async_to_sync
from celery import Celery
from dependency_injector.wiring import inject, Provide

from services.amount_ads_observer.dal import AdsObserversRepository, AdsObserversStatRepository
from services.amount_ads_observer.schemas.ads_observer_stat import AdsObserverStatCreate
from services.private_avito_api_executor.private_avito_api_executor_pb2 import GetAmountAdsRequest
from services.private_avito_api_executor.grpc.client import PrivateAvitoApiExecutorGrpcClient
from services.worker.config import worker_settings
from services.worker.container import WorkerContainer
from utils.datetime import get_uts_from_datetime

celery = Celery(
    'tasks',
    broker=worker_settings.celery_broker_url,
    backend=worker_settings.celery_result_backend
)


@celery.on_after_configure.connect
def init_di_container(sender, **kwargs):
    worker_container = WorkerContainer()
    worker_container.wire(modules=[__name__])


@celery.task
@inject
def save_curr_ads_amount(
        ads_observer_id: int,
        location_id: int,
        query: str,
        ads_observers_repository: AdsObserversRepository = Provide[WorkerContainer.ads_observers_repository],
        ads_observers_stats_repository: AdsObserversStatRepository =
        Provide[WorkerContainer.ads_observers_stats_repository],
        private_avito_api_executor_client: PrivateAvitoApiExecutorGrpcClient =
        Provide[WorkerContainer.private_avito_api_executor_client]
):
    exists = async_to_sync(ads_observers_repository.get_by_id)(ads_observer_id)
    if not exists:
        return

    req = GetAmountAdsRequest(
        location_id=location_id,
        query=query
    )
    # TODO: handle errors
    res = private_avito_api_executor_client.stub.get_amount_ads(req)

    now = datetime.utcnow()
    uts_now = get_uts_from_datetime(now)
    new_ads_observer_stat = AdsObserverStatCreate(
        ads_observer_id=ads_observer_id,
        timestamp=uts_now,
        amount=res.amount
    )
    async_to_sync(ads_observers_stats_repository.add_one)(new_ads_observer_stat)

    in_hour = now + timedelta(minutes=1)
    save_curr_ads_amount.apply_async(
        (
            ads_observer_id,
            location_id,
            query
        ),
        eta=in_hour
    )
