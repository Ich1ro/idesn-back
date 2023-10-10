from asyncpg import connection
from dacite import from_dict
from data.repository import Repository
from models.artifact_variable import ArtifactVariable


class ArtifactVariableRepository(Repository):
    def __init__(self, connection: connection.Connection) -> None:
        super().__init__(connection)

    async def fetch_one_by_filter(self, artifact_filter: dict[str, tuple[str, any]]) -> ArtifactVariable:
        command = """
        SELECT ID, TEMPLATE_ID, QUIZ_ID, INPUT, NAME, VALUE
        FROM ARTIFACT_VARIABLE
        """
        index = 1
        for key, sign, _ in artifact_filter.items():
            command += f" {key.upper()} {sign} ${index} AND"
            index += 1
        command = command.rstrip("AND")
        values = [value for _, value in artifact_filter.values()]
        record = await self._connection.fetchrow(command, *values)
        return from_dict(data_class=ArtifactVariable, data=dict(record.items()))

    async def insert(self, artifact_variable: ArtifactVariable) -> ArtifactVariable:
        command = """
        INSERT INTO ARTIFACT(TEMPLATE_ID, QUIZ_ID, INPUT, NAME, VALUE)
        SELECT $1, $2, $3, $4, $5
        RETURNING ID;
        """
        id = await self._connection.fetchval(command, artifact_variable.template_id, artifact_variable.quiz_id, artifact_variable.input, artifact_variable.name, artifact_variable.value)
        return await self.fetch_one_by_filter({"id": ("=", id)})

    async def update(self, id: int, artifact_variable: dict[str, any]) -> ArtifactVariable:
        command = "UPDATE ARTIFACT SET"

        index = 1
        for key in artifact_variable.keys():
            command += f" {key.upper()} = ${index},"
            index += 1
        command.rstrip(",")

        command += f"""
        WHERE ID = ${index};
        """
        _ = await self._connection.execute(command, *artifact_variable.values(), id)
        return await self.fetch_one_by_filter({"id": ("=", id)})
