from models.DTOs.start_quiz_dto import StartQuizDto
from models.quiz import Quiz
from data.unit_of_work import UnitOfWork


class QuizService:
    _uof: UnitOfWork

    def __init__(self, uof: UnitOfWork) -> None:
        self._uof = uof

    async def start(self, dto: StartQuizDto) -> Quiz:
        model = Quiz(
            id=None,
            template_id=dto.template_id
        )
        return await self._uof.quizzes.insert(model)
