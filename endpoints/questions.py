from fastapi import APIRouter
from data.unit_of_work import UnitOfWork
from data.vault_client import VaultClient
from services.quiz_questions_service import QuizQuestionService


router = APIRouter(prefix="/api/v1/quizzes/questions")


@router.get("/")
async def get():
    vault_client = VaultClient()
    service = QuizQuestionService(
        UnitOfWork(vault_client)
    )
    return await service.get()
