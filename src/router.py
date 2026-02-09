from .apis import Depositar, DSW

from fastapi import FastAPI, Request
import fastapi
import itertools
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


@app.post("/generate_dsw_documents_from_project={qry}")
async def generate_dsw_documents_from_project(
    qry: str,
    request: Request,
) -> dict:
    all_headers = dict(request.headers)

    try:
        dsw_project_list: dict = await DSW.get_project_list(qry, request.headers)
        projects: dict = dsw_project_list["_embedded"]["projects"]
        project_metadatas: list = []
        for project in projects:
            project_metadatas.append(
                [project["name"], project["permissions"][0]["projectUuid"]]
            )

        document_template_metadatas = [
            ["dsw:questionnaire-report:2.16.1", "HTML Document"],
            ["dsw:science-europe:1.29.1", "HTML Document"],
            ["dsw:rda-madmp:1.27.1", "RDF/XML"],
        ]
        for metadata in document_template_metadatas:
            format_uuid: str = await DSW.get_format_uuid(metadata, request.headers)
            metadata.append(format_uuid)

        for p_metadata, d_metadata in itertools.product(
            project_metadatas, document_template_metadatas
        ):
            await DSW.create_documents(p_metadata, d_metadata, request.headers)

        headers: dict = {}
        return fastapi.responses.JSONResponse(
            headers=headers,
            status_code=fastapi.status.HTTP_201_CREATED,
            content={
                "message": "Generate documents successfully!",
            },
        )
    except Exception as e:
        print(traceback.format_exc())
        return fastapi.responses.PlainTextResponse(
            status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=f"Could not send the notification ({type(e).__name__}).\n\n"
            f"{str(e)}.\n",
        )

@app.post("/submit_dsw_documents_from_project={qry}")
async def submit_dsw_documents_from_project(
    qry: str,
    request: Request,
) -> dict:
    all_headers = dict(request.headers)

    try:
        '''
        document_template_metadatas = [
            ["dsw:questionnaire-report:2.16.1", "HTML Document"],
            ["dsw:science-europe:1.29.1", "HTML Document"],
            ["dsw:rda-madmp:1.27.1", "RDF/XML"],
        ]
        for metadata in document_template_metadatas:
            format_uuid: str = await DSW.get_format_uuid(metadata, request.headers)
            metadata.append(format_uuid)
        '''
        documents: dict = await DSW.get_document_info(request.headers, qry)

        for document in documents:
            if document[2] == "RDF/XML":
                await DSW.submit_madmp(document[3], {"serviceId": "depositar_submit_madmp"})
        for document in documents:
            if document[2] == "HTML Document":
                await DSW.submit_html(document[3], {"serviceId": "depositar_submit_html"})

        headers: dict = {}
        return fastapi.responses.JSONResponse(
            headers=headers,
            status_code=fastapi.status.HTTP_201_CREATED,
            content={
                "message": "Generate documents successfully!",
            },
        )
    except Exception as e:
        print(traceback.format_exc())
        return fastapi.responses.PlainTextResponse(
            status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=f"Could not send the notification ({type(e).__name__}).\n\n"
            f"{str(e)}.\n",
        )


@app.post("/submit_madmp")
async def submit_madmp(
    request: Request,
) -> dict:
    all_headers: dict = dict(request.headers)
    body_bytes: bytes = await request.body()
    body_str: str = body_bytes.decode("utf-8")
    headers: dict = {}

    try:
        await Depositar.submit_madmp(all_headers, body_str)
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

@app.post("/submit_html")
async def submit_html(
    request: Request,
) -> dict:
    all_headers: dict = dict(request.headers)
    body_bytes: bytes = await request.body()
    body_str: str = body_bytes.decode("utf-8")
    headers: dict = {}

    try:
        await Depositar.submit_html(all_headers, body_str)
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