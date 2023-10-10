from fastapi import APIRouter
from data.data_lake_client import DataLakeClient
from services.page_template_reader import PageTemplateReader
from data.unit_of_work import UnitOfWork
from data.vault_client import VaultClient


router = APIRouter(prefix="/api/v1/templates")


@router.get("/{template_id}")
async def get_template(template_id: int):
    vault_client = VaultClient()
    return await PageTemplateReader(
        UnitOfWork(vault_client),
        DataLakeClient(vault_client, container_name="templates")
    ).get(template_id)
