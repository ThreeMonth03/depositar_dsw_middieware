from .base import Base_Get_Project_List

from fastapi import Request
from requests import Response
import requests


class ROR_Get_Project_List(Base_Get_Project_List):
    __url: str = "https://api.ror.org/organizations"

    @classmethod
    async def get_project_list(cls, query: str, headers: Request) -> dict:
        safe_headers: dict = {
            "User-Agent": headers.get("user-agent", "FastAPI-App/1.0"),
            "client-id": headers.get("client-id", ""),
            "x-identity": headers.get("x-identity", ""),
            "Accept": "application/json",
        }
        params: dict = {"query": query}

        response: Response = requests.get(
            cls.__url, params=params, headers=safe_headers
        )

        return response.json()
