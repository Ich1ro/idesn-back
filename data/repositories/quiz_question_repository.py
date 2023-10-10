from asyncpg import connection
from dacite import from_dict
from data.repository import Repository
from models.quiz_question import QuizQuestion


class QuizQuestionRepository(Repository):
    def __init__(self, connection: connection.Connection) -> None:
        super().__init__(connection)

    async def fetch_by_filter(self, filter: dict[str, tuple[str, any]] = None) -> list[QuizQuestion]:
        command = """
        SELECT ID, QUESTION_ID, VARIABLE, TYPE, QUESTION, DESCRIPTION
        FROM QUIZ_QUESTION
        """
        values = []
        if filter:
            command += " WHERE"
            index = 1
            for key, (sign, _) in filter.items():
                command += f" {key.upper()} {sign} ${index} AND"
                index += 1
            command = command.rstrip("AND")
            values = [value for _, value in filter.values()]

        records = await self._connection.fetch(command, *values)

        return [
            from_dict(data_class=QuizQuestion, data=dict(record.items()))
            for record in records
        ]
