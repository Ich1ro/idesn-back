from fastapi import APIRouter
from clients.replicate_client import DiffusionClient
from data.data_lake_client import DataLakeClient
from data.unit_of_work import UnitOfWork
from data.vault_client import VaultClient
from models.DTOs.generate_dto import GenerateDto
from services.image_service import ImageService


router = APIRouter(prefix="/api/v1/images")


@router.post("/generate")
async def generate_image(dto: GenerateDto):
    vault_client = VaultClient()
    image_service = ImageService(
        UnitOfWork(vault_client),
        DiffusionClient(width=768, height=768, num_outputs=1),
        DataLakeClient(vault_client, container_name="images")
    )
    return await image_service.generate_image(dto)
