"""
Announcement observer service entrypoint.
"""
from fastapi import FastAPI

from services.amount_ads_observer.container import \
    AmountAdsObserverContainer
from services.amount_ads_observer.routers import api_router
from services.amount_ads_observer.utils import async_init_db

app = FastAPI()
app.include_router(api_router)
container = AmountAdsObserverContainer()


@app.on_event('startup')
async def wire_container():
    container.wire(
        modules=[__name__],
        packages=['.routers']
    )


@app.on_event('startup')
async def init_db():
    await async_init_db(container.db())
