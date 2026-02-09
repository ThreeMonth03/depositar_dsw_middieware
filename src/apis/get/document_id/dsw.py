from fastapi import Request
import os
from requests import Response
import requests
from typing import Any


class DSWGetDocumentInfo:
    __url: str = "http://server:3000/wizard-api/documents"

    @classmethod
    async def get_document_info(
        cls, header: dict[str, Any], document_name: str
    ) -> list:
        safe_headers: dict[str, Any] = {
            "Accept": "application/json",
            "Authorization": f"Bearer {os.getenv("DSW_ROOT_KEY")}",
        }
        params: dict[str, Any] = {"q": document_name}
        response: Response = requests.get(
            cls.__url, params=params, headers=safe_headers
        )
        print(response.json())
        documents = response.json()["_embedded"]["documents"]
        ret = []
        for document in documents:
            project_name = document["project"]["name"]
            document_template_id = document["documentTemplateId"]
            document_template_type = document["format"]["name"]
            document_uuid = document["uuid"]
            ret.append(
                [
                    project_name,
                    document_template_id,
                    document_template_type,
                    document_uuid,
                ]
            )
        print(ret)
        return ret
