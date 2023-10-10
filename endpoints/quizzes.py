from fastapi import APIRouter
from data.unit_of_work import UnitOfWork
from data.vault_client import VaultClient
from models.DTOs.start_quiz_dto import StartQuizDto
from services.quiz_service import QuizService


router = APIRouter(prefix="/api/v1/quizzes")


@router.post("/")
async def post(dto: StartQuizDto):
    vault_client = VaultClient()
    service = QuizService(
        UnitOfWork(vault_client)
    )
    return await service.start(dto)
