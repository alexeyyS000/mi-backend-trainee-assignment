"""
Announcement service routers.
"""
from fastapi import APIRouter

from services.amount_ads_observer.routers import amount_ads_observer

api_router = APIRouter(prefix='/api')
api_router.include_router(amount_ads_observer.router)
