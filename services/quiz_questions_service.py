from data.unit_of_work import UnitOfWork
from models.quiz_question import QuizQuestion


class QuizQuestionService:
    _uof: UnitOfWork

    def __init__(self, uof: UnitOfWork) -> None:
        self._uof = uof

    async def get(self) -> list[QuizQuestion]:
        async with self._uof:
            return await self._uof.quiz_questions.fetch_by_filter()
