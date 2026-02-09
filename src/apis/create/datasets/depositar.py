from io import StringIO
import requests
from typing import Any


class DepositarCreateDatasets:
    __url = "https://demo.depositar.io/api/3/action/package_create"

    @classmethod
    async def create_datasets(
        cls,
        dataset_json: dict[str, Any],
        auth_headers: dict[str, Any],
    ) -> None:
        response = requests.post(cls.__url, json=dataset_json, headers=auth_headers)
        print(response.json())