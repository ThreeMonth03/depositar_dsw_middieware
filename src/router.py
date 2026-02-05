from .apis import Depositar

from fastapi import FastAPI, Request
import fastapi
import traceback

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


@app.post("/submit_questionnaire")
async def submit_questionnaire(
    request: Request,
) -> dict:
    all_headers: dict = dict(request.headers)
    body_bytes: bytes = await request.body()
    body_str: str = body_bytes.decode("utf-8")
    headers: dict = {}
    try:
        await Depositar.create_resources(all_headers, body_str)
        return fastapi.responses.JSONResponse(
            headers=headers,
            status_code=fastapi.status.HTTP_201_CREATED,
            content={
                "message": "Notification sent successfully!",
            },
        )
    except Exception as e:
        print(traceback.format_exc())
        return fastapi.responses.PlainTextResponse(
            status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=f"Could not send the notification ({type(e).__name__}).\n\n"
            f"{str(e)}.\n",
        )
