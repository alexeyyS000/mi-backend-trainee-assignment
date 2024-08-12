"""
Private Avito API executor GRPC server.
"""
from typing import Optional
import urllib

from playwright.async_api import Playwright, Browser, Page

from services.private_avito_api_executor.config import private_avito_api_executor_settings
from services.private_avito_api_executor.private_avito_api_executor_pb2 import GetAmountAdsResponse
from services.private_avito_api_executor.private_avito_api_executor_pb2_grpc import PrivateAvitoApiExecutorServicer
from services.private_avito_api_executor.schemas.items import AvitoItemsResponse, AvitoItemsRequest
from utils.playwright.request import make_async_get_request


class AsyncPrivateAvitoApiExecutorService(
    PrivateAvitoApiExecutorServicer
):
    def __init__(self, playwright: Playwright):
        super().__init__()

        self.playwright = playwright
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None

    async def get_amount_ads(self, request, context):
        req = AvitoItemsRequest(
            key=private_avito_api_executor_settings.avito_magic_key,
            locationId=request.location_id,
            query=request.query
        )
        url = 'https://m.avito.ru/api/11/items?'
        url += urllib.parse.urlencode(req.dict(by_alias=True))
        response = await make_async_get_request(self.page, url, AvitoItemsResponse)
        return GetAmountAdsResponse(amount=response.result.count)

    async def run_browser(self):
        self.browser = await self.playwright.chromium.launch()
        self.page = await self.browser.new_page()
        return self

    async def finalize(self):
        await self.browser.close()
