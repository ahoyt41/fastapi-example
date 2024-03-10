from fastapi_example.config import config
from fastapi_example.service import MockService


class ServiceDepedency:
    def __init__(self, svc: MockService):
        self.svc = svc

    def __call__(self) -> MockService:
        return self.svc


svc_dep = ServiceDepedency(MockService(config.db_file))
