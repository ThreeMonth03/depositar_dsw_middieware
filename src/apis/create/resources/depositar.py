from fastapi import Request
import fastapi
from io import StringIO
import io
import json
from rdflib import Graph
from requests import Response
import requests
from typing import Any


class Depositar_Create_Resources:
    __upload_url: dict[str, str] = {
        "dataset": "https://demo.depositar.io/api/3/action/package_create",
        "resources": "https://demo.depositar.io/api/3/action/resource_create",
    }
    __query_url: str = "https://demo.depositar.io/api/3/action/package_show"

    @classmethod
    async def create_resources(cls, header: dict, body: str) -> None:
        rdf_dict: dict[str, Any] = cls.__rdf_to_json_ld(body)
        rdf_info: dict[str, Any] = cls.__extract_json_ld(rdf_dict)

        try:
            await cls.__create_dataset(header, rdf_info)
        except:
            pass

        dataset_id: str = await cls.__get_dataset_id(header, rdf_info["project_name"])

        await cls.__create_resources(header, body, rdf_info, dataset_id)

    @classmethod
    def __rdf_to_json_ld(cls, body: str) -> dict[str, Any]:
        g: Graph = Graph()
        g.parse(data=body, format="xml")
        json_ld_str: str = g.serialize(format="json-ld", indent=2, auto_compact=True)
        data: dict[str, Any] = json.loads(json_ld_str)
        return data

    @classmethod
    def __extract_json_ld(cls, rdf_dict: dict[str, Any]) -> dict[str, Any]:
        rdf_info: dict[str, Any] = {"author_name": [], "author_email": []}
        graph: list[dict[str, Any]] = rdf_dict["@graph"]
        for node in graph:
            if node["@type"] == "dcso:Contact":
                rdf_info["contact_email"] = node["foaf:mbox"]
                rdf_info["contact_name"] = node["foaf:name"]
            if node["@type"] == "dcso:Contributor":
                rdf_info["author_email"].append(node["foaf:mbox"])
                rdf_info["author_name"].append(node["foaf:name"])
            if node["@type"] == "dcso:DMP":
                rdf_info["project_name"] = node["dcterms:title"]
                rdf_info["resource_description"] = node["dcterms:description"]
                rdf_info["project_description"] = (
                    f"{node["dcterms:description"].split('. ', 1)[0]}."
                )
        return rdf_info

    @classmethod
    async def __create_dataset(
        cls, header: dict[str, Any], rdf_info: dict[str, Any]
    ) -> None:
        url: str = cls.__upload_url["dataset"]
        dataset_json: dict[str, Any] = cls.__dataset_json(rdf_info)
        auth_headers: dict[str, Any] = cls.__auth_headers(header)
        requests.post(url, json=dataset_json, headers=auth_headers)

    @classmethod
    async def __get_dataset_id(cls, header: dict[str, Any], project_name: str) -> str:
        safe_headers: dict[str, Any] = {
            "User-Agent": header.get("user-agent", "FastAPI-App/1.0"),
            "depositar-api-key": header.get("depositar-api-key", ""),
            "x-identity": header.get("x-identity", ""),
            "Accept": "application/json",
        }
        params: dict[str, Any] = {"id": project_name}

        response: Response = requests.get(
            cls.__query_url, params=params, headers=safe_headers
        )
        response_json: dict[str, Any] = response.json()
        return response_json["result"]["id"]

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
        response: Response = requests.post(
            url, data=resource_json, files=files, headers=auth_headers
        )

    @classmethod
    def __auth_headers(cls, header: dict[str, Any]) -> dict[str, Any]:
        headers: dict[str, Any] = {
            "Authorization": header["depositar-api-key"],
        }
        return headers

    @classmethod
    def __dataset_json(cls, rdf_info: dict[str, Any]) -> dict[str, Any]:
        dataset_json: dict[str, Any] = {
            "author": ", ".join(rdf_info["author_name"]),
            "contact_email": rdf_info["contact_email"],
            "contact_person": rdf_info["contact_name"],
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
