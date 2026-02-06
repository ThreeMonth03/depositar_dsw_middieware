from fastapi import Request
import os
from requests import Response
import requests


class DSW_Get_Format_Uuid:
    __url: str = "http://server:3000/wizard-api/document-templates"

    @classmethod
    async def get_format_uuid(cls, metadata: list[str], headers: Request) -> str:
        safe_headers: dict = {
            "Accept": "application/json",
            "Authorization": f"Bearer {os.getenv("DSW_ROOT_KEY")}",
        }

        response: Response = requests.get(
            f"{cls.__url}/{metadata[0]}", headers=safe_headers
        )
        formats: list = response.json()["formats"]
        format_uuid = ""
        for format in formats:
            if format["name"] == metadata[1]:
                format_uuid = format["uuid"]
        return format_uuid
