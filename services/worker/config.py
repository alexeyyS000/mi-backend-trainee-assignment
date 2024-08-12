"""
Worker configuration.
"""
from pydantic import BaseSettings


class WorkerSettings(BaseSettings):
    private_avito_api_executor_grpc_server_addr: str = 'localhost:50051'

    # Celery
    celery_broker_url: str = 'redis://localhost:6379'
    celery_result_backend: str = 'redis://localhost:6379'


worker_settings = WorkerSettings()
