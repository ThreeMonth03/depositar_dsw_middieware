from .apis import Depositar

from fastapi import FastAPI, Response, Request
import fastapi
import traceback
from typing import Optional
import uuid

app: FastAPI = FastAPI()


@app.get("/")
def hello_world() -> str:
    return "Welcome to use depositar router api."


@app.get("/get_project_list={qry}")
async def get_project_list(
    qry: str,
    request: Request,
) -> dict:
    all_headers = dict(request.headers)

    depositar_return: dict = await Depositar.get_project_list(qry, request.headers)
    return depositar_return
