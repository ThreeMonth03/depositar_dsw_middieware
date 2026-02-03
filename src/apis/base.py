import abc
from fastapi import Request


class ApiBase(abc.ABC):
    @classmethod
    @abc.abstractmethod
    async def request(cls, query: str, headers: Request):
        return NotImplemented
