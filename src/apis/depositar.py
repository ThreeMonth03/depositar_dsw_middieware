from src.apis import ApiBase
from fastapi import Request
from requests import Response
import requests


class Depositar(ApiBase):
    url = "https://data.depositar.io/api/3/action/package_search"

    @classmethod
    async def request(cls, query: str, headers: Request) -> dict:
        safe_headers: dict = {
            "User-Agent": headers.get("user-agent", "FastAPI-App/1.0"),
            "depositar-api-key": headers.get("depositar-api-key", ""),
            "x-identity": headers.get("x-identity", ""),
            "Accept": "application/json",
        }
        params: dict = {"q": query}

        response: Response = requests.get(cls.url, params=params, headers=safe_headers)

        return response.json()
