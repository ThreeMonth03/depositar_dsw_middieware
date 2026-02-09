from fastapi import Request
import fastapi
from io import StringIO
import io
import json
from requests import Response
import requests
from typing import Any
import os


class DSWSubmitHtml:
    __url = "http://server:3000/wizard-api/documents/"
    __action = "/submissions"

    @classmethod
    async def submit_html(
        cls, uuid: str, files: dict[str, tuple[str, StringIO, str]]
    ) -> None:
        safe_headers: dict[str, Any] = {
            "Accept": "application/json",
            "Authorization": f"Bearer {os.getenv("DSW_ROOT_KEY")}",
        }
        response = requests.post(
            f"{cls.__url}{uuid}{cls.__action}", json=files, headers=safe_headers
        )
        # print(response.json())
