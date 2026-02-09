from src.data_parser import RdfParser

from fastapi import Request
import fastapi
from io import StringIO
import io
import json
from requests import Response
import requests
from typing import Any


class DepositarSubmitMaDMP:
    __upload_url: dict[str, str] = {
        "dataset": "https://demo.depositar.io/api/3/action/package_create",
        "resources": "https://demo.depositar.io/api/3/action/resource_create",
    }

    @classmethod
    async def submit_madmp(cls, header: dict, body: str) -> None:
        rdf_dict: dict[str, Any] = RdfParser.rdf_to_json_ld(body)
        rdf_info: dict[str, Any] = RdfParser.extract_json_ld(rdf_dict)
        if True:
            #try:
            await cls.__create_dataset(header, rdf_info)
        else:
            #except:
            pass
        dataset_id: str = await cls.get_dataset_id(header, rdf_info["project_name"])

        await cls.__create_resources(header, body, rdf_info, dataset_id)

    @classmethod
    async def __create_dataset(
        cls, header: dict[str, Any], rdf_info: dict[str, Any]
    ) -> None:
        url: str = cls.__upload_url["dataset"]
        dataset_json: dict[str, Any] = cls.__dataset_json(rdf_info)
        auth_headers: dict[str, Any] = cls.__auth_headers(header)
        await cls.create_datasets(dataset_json = dataset_json, auth_headers = auth_headers)

    @classmethod
    async def __create_resources(
        cls,
        header: dict[str, Any],
        body: str,
        rdf_info: dict[str, Any],
        dataset_id: str,
    ) -> None:
        url: str = cls.__upload_url["resources"]
        resource_json: dict[str, Any] = cls.__resource_json(rdf_info, dataset_id)
        auth_headers: dict[str, Any] = cls.__auth_headers(header)
        files: dict[str, tuple[str, StringIO, str]] = cls.__wrap_files(body, rdf_info)
        await cls.create_resources(data=resource_json, files=files, headers=auth_headers)

    @classmethod
    def __auth_headers(cls, header: dict[str, Any]) -> dict[str, Any]:
        headers: dict[str, Any] = {
            "Authorization": header["depositar-api-key"],
        }
        return headers

    @classmethod
    def __dataset_json(cls, rdf_info: dict[str, Any]) -> dict[str, Any]:
        authors = rdf_info.get("author_name", [])
        author_value = ", ".join(authors) if authors else "TEST_NAME"
        dataset_json: dict[str, Any] = {
            "author": author_value,
            "contact_email": rdf_info.get("contact_email", ""),
            "contact_person": rdf_info.get("contact_name", ""),
            "data_type": ["structured"],
            "keywords": [],
            "language": [],
            "license_id": "cc-by",
            "license_title": "CC-BY 4.0",
            "name": rdf_info["project_name"],
            "notes": rdf_info["project_description"],
            "owner_org": "dsw_project",
            "process_step": "",
            "remarks": "",
            "state": "active",
            "title": rdf_info["project_name"],
            "type": "dataset",
        }

        return dataset_json

    @classmethod
    def __resource_json(
        cls, rdf_info: dict[str, Any], dataset_id: str
    ) -> dict[str, Any]:
        resource_json: dict[str, Any] = {
            "package_id": dataset_id,
            "name": f"{rdf_info["project_name"]}_{'_'.join(rdf_info["author_name"])}.rdf",
            "format": "RDF",
            "description": rdf_info["resource_description"],
        }
        return resource_json

    @classmethod
    def __wrap_files(cls, body: bytes, rdf_info: dict[str, Any]) -> dict[str, Any]:
        files: dict[str, Any] = {
            "upload": (
                f"{rdf_info["project_name"]}_{'_'.join(rdf_info["author_name"])}",
                io.StringIO(body),
                "application/rdf+xml",
            )
        }
        return files
