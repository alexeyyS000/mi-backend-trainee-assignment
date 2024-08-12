"""
gRPC Private Avito API executor client.
"""
from utils.grpc.client import GrpcClient

from services.private_avito_api_executor.private_avito_api_executor_pb2_grpc import PrivateAvitoApiExecutorStub


class PrivateAvitoApiExecutorGrpcClient(GrpcClient):
    def __init__(self, addr: str):
        super().__init__(addr, PrivateAvitoApiExecutorStub)
