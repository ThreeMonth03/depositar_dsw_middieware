from .base import Base_Get_Project_List

from fastapi import Request
from requests import Response
import requests


class Depositar_Get_Project_List(Base_Get_Project_List):
    __url: str = "https://data.depositar.io/api/3/action/package_search"

    @classmethod
    async def get_project_list(cls, query: str, headers: Request) -> dict:
        safe_headers: dict = {
            "User-Agent": headers.get("user-agent", "FastAPI-App/1.0"),
            "depositar-api-key": headers.get("depositar-api-key", ""),
            "x-identity": headers.get("x-identity", ""),
            "Accept": "application/json",
        }
        params: dict = {"q": query}

        response: Response = requests.get(
            cls.__url, params=params, headers=safe_headers
        )

        return response.json()
