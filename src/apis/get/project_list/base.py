import abc
from fastapi import Request


class Base_Get_Project_List(abc.ABC):
    @classmethod
    @abc.abstractmethod
    async def get_project_list(cls, query: str, headers: Request):
        return NotImplemented
