from src.apis import ApiBase
from fastapi import Request
from requests import Response
import requests


class ROR(ApiBase):
    url = "https://api.ror.org/organizations"

    @classmethod
    async def request(cls, query: str, headers: Request) -> dict:
        safe_headers: dict = {
            "User-Agent": headers.get("user-agent", "FastAPI-App/1.0"),
            "client-id": headers.get("client-id", ""),
            "x-identity": headers.get("x-identity", ""),
            "Accept": "application/json",
        }
        params: dict = {"query": query}

        response: Response = requests.get(cls.url, params=params, headers=safe_headers)

        return response.json()
