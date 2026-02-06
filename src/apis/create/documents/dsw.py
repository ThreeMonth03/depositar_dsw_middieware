from fastapi import Request
import os
from requests import Response
import requests


class DSW_Create_Documents:
    __url: str = "http://server:3000/wizard-api/documents"

    @classmethod
    async def create_documents(
        cls,
        project_metadata: list[str],
        document_template_metadata: list[str],
        headers: Request,
    ) -> None:
        safe_headers: dict = {
            "Accept": "application/json",
            "Authorization": f"Bearer {os.getenv("DSW_ROOT_KEY")}",
        }
        body = {
            "documentTemplateId": document_template_metadata[0],
            "formatUuid": document_template_metadata[2],
            "name": f"{project_metadata[0]}_{document_template_metadata[0]}_{document_template_metadata[1]}",
            "projectUuid": project_metadata[1],
        }
        response: Response = requests.post(cls.__url, headers=safe_headers, json=body)
