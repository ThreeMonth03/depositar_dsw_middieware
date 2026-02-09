import json
from rdflib import Graph
from typing import Any


class RdfParser:
    @staticmethod
    def rdf_to_json_ld(body: str) -> dict[str, Any]:
        g: Graph = Graph()
        g.parse(data=body, format="xml")
        json_ld_str: str = g.serialize(format="json-ld", indent=2, auto_compact=True)
        data: dict[str, Any] = json.loads(json_ld_str)
        return data

    @staticmethod
    def extract_json_ld(rdf_dict: dict[str, Any]) -> dict[str, Any]:
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
