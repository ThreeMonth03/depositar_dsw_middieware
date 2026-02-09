from src.data_parser import RdfParser

from fastapi import Request
import fastapi
from io import StringIO
import io
import json
from requests import Response
import requests
from typing import Any


class DepositarSubmitHtml:
    __upload_url: dict[str, str] = {
        "dataset": "https://demo.depositar.io/api/3/action/package_create",
        "resources": "https://demo.depositar.io/api/3/action/resource_create",
    }

    @classmethod
    async def submit_html(cls, header: dict, body: str) -> None:
        print("Not implemented")
        pass
