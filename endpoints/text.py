from fastapi import APIRouter
from clients.description_generator import DescriptionGenerator
from data.unit_of_work import UnitOfWork
from data.vault_client import VaultClient
from models.DTOs.generate_dto import GenerateDto
from services.text_service import TextService


router = APIRouter(prefix="/api/v1/text")


@router.post("/generate")
async def generate_text(dto: GenerateDto):
    vault_client = VaultClient()
    text_generator = TextService(
        UnitOfWork(vault_client),
        DescriptionGenerator()
    )
    text = await text_generator.generate_text(dto)
    return {
        "text": text
    }
