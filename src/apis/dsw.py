from .create import DSW_Create_Documents
from .get import DSWGetDocumentInfo, DSW_Get_Format_Uuid, DSW_Get_Project_List
from .submit import DSWSubmitHtml, DSWSubmitMaDMP


class DSW(
    DSW_Create_Documents,
    DSWGetDocumentInfo,
    DSW_Get_Format_Uuid,
    DSW_Get_Project_List,
    DSWSubmitHtml,
    DSWSubmitMaDMP,
):
    pass
