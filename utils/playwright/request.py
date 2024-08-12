"""
Playwright request utils.
"""
from typing import Type, TypeVar, Optional

from playwright.async_api import Page
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)


async def make_async_get_request(page: Page, url: str, schema_type: Type[T]) -> Optional[T]:
    """
    Make GET request by Playwright.

    :param schema_type: Pydantic schema
    :param page: Playwright page
    :param url: URL
    :return: Schema instance
    """
    response = await page.goto(url, wait_until='load')
    if not response:
        return None

    content = await response.body()
    return schema_type.parse_raw(content)
