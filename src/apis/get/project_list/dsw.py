from .base import Base_Get_Project_List

from fastapi import Request
import os
from requests import Response
import requests


class DSW_Get_Project_List(Base_Get_Project_List):
    __url: str = "http://server:3000/wizard-api/projects"

    @classmethod
    async def get_project_list(cls, query: str, headers: Request) -> dict:
        safe_headers: dict = {
            "Accept": "application/json",
            "Authorization": f"Bearer {os.getenv("DSW_ROOT_KEY")}",
        }
        params: dict = {"q": query}

        response: Response = requests.get(
            cls.__url, params=params, headers=safe_headers
        )
        return response.json()
