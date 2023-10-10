from asyncpg import connection
from dacite import from_dict
from data.repository import Repository
from models.quiz import Quiz


class QuizRepository(Repository):
    def __init__(self, connection: connection.Connection) -> None:
        super().__init__(connection)

    async def fetch_one_by_filter(self, artifact_filter: dict[str, tuple[str, any]]) -> Quiz:
        command = """
        SELECT ID, TEMPLATE_ID
        FROM QUIZ
        WHERE
        """
        index = 1
        for key, (sign, _) in artifact_filter.items():
            command += f" {key.upper()} {sign} ${index} AND"
            index += 1
        command = command.rstrip("AND")
        values = [value for _, value in artifact_filter.values()]
        record = await self._connection.fetchrow(command, *values)
        return from_dict(data_class=Quiz, data=dict(record.items()))

    async def insert(self, model: Quiz) -> Quiz:
        command = """
        INSERT INTO QUIZ(TEMPLATE_ID)
        SELECT $1
        RETURNING ID;
        """
        id = await self._connection.fetchval(command, model.template_id)
        return await self.fetch_one_by_filter({"id": ("=", id)})
