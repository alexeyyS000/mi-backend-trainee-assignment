"""
Private Avito API executor service entrypoint.
"""
import asyncio

from grpc import aio
from loguru import logger
from playwright.async_api import Playwright, async_playwright

from services.private_avito_api_executor import private_avito_api_executor_pb2_grpc
from services.private_avito_api_executor.grpc.server import AsyncPrivateAvitoApiExecutorService
from services.private_avito_api_executor.config import private_avito_api_executor_settings


async def run_grpc_server(playwright: Playwright):
    """
    Run gRPC server.

    :param playwright: Playwright instance
    """
    server = aio.server()

    service = AsyncPrivateAvitoApiExecutorService(playwright)
    await service.run_browser()

    private_avito_api_executor_pb2_grpc.add_PrivateAvitoApiExecutorServicer_to_server(
        service,
        server
    )
    server.add_insecure_port(private_avito_api_executor_settings.grpc_server_addr)

    logger.info(f'starting gRPC server on {private_avito_api_executor_settings.grpc_server_addr}')
    await server.start()
    await server.wait_for_termination()

    await service.finalize()


async def main():
    """
    Service entrypoint.
    """
    async with async_playwright() as playwright:
        await run_grpc_server(playwright)


if __name__ == '__main__':
    asyncio.run(main())
