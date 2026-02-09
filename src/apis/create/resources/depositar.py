from io import StringIO
import requests
from typing import Any


class DepositarCreateResources:
    __url = "https://demo.depositar.io/api/3/action/resource_create"

    @classmethod
    async def create_resources(
        cls,
        data: dict[str, Any],
        files: dict[str, tuple[str, StringIO, str]],
        headers: dict[str, Any],
    ) -> None:
        requests.post(cls.__url, data=data, files=files, headers=headers)
