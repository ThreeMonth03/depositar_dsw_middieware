from src.apis import ROR, Depositar
from fastapi import FastAPI, Response, Request
from typing import Optional

app: FastAPI = FastAPI()


@app.get("/")
def hello_world() -> str:
    return "Welcome to use depositar router api."


@app.get("/router_query={qry}")
async def router_query(
    qry: str,
    request: Request,
) -> dict:
    all_headers = dict(request.headers)

    print("--- User Headers ---")
    for key, value in all_headers.items():
        print(f"{key}: {value}")
    print("------------------------------")

    depositar_return: dict = await Depositar.request(qry, request.headers)
    return depositar_return
