from .create import DSW_Create_Documents
from .get import DSW_Get_Project_List, DSW_Get_Format_Uuid


class DSW(DSW_Create_Documents, DSW_Get_Project_List, DSW_Get_Format_Uuid):
    pass
