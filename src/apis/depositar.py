from .create import DepositarCreateResources, DepositarCreateDatasets
from .get import Depositar_Get_Project_List, DepositarGetDatasetId
from .submit import DepositarSubmitHtml, DepositarSubmitMaDMP


class Depositar(
    DepositarCreateResources,
    DepositarCreateDatasets,
    DepositarGetDatasetId,
    Depositar_Get_Project_List,
    DepositarSubmitHtml,
    DepositarSubmitMaDMP,
):
    pass
