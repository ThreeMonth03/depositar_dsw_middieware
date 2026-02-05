from .get import Depositar_Get_Project_List
from .create import Depositar_Create_Resources


class Depositar(Depositar_Get_Project_List, Depositar_Create_Resources):
    pass
