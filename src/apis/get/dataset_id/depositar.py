from fastapi import Request
import os
from requests import Response
import requests
from typing import Any

class DepositarGetDatasetId:
    __url: str = "https://demo.depositar.io/api/3/action/package_show"

    @classmethod
    async def get_dataset_id(cls, header: dict[str, Any], project_name: str) -> str:
        safe_headers: dict[str, Any] = {
            "User-Agent": header.get("user-agent", "FastAPI-App/1.0"),
            "depositar-api-key": header.get("depositar-api-key", ""),
            "x-identity": header.get("x-identity", ""),
            "Accept": "application/json",
        }
        params: dict[str, Any] = {"id": project_name}
        response: Response = requests.get(
            cls.__url, params=params, headers=safe_headers
        )
        response_json: dict[str, Any] = response.json()
        return response_json["result"]["id"]