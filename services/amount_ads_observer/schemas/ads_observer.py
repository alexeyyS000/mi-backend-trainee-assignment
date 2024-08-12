from pydantic import BaseModel


class BaseAdsObserver(BaseModel):
    location_id: int
    query: str


class AdsObserverCreate(BaseAdsObserver):
    pass


class AdsObserver(BaseAdsObserver):
    id: int

    class Config:
        orm_mode = True
