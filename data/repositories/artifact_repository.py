from asyncpg import connection
from dacite import from_dict
from data.repository import Repository
from models.artifact import Artifact


class ArtifactRepository(Repository):
    def __init__(self, connection: connection.Connection) -> None:
        super().__init__(connection)

    async def fetch_one_by_filter(self, artifact_filter: dict[str, tuple[str, any]]) -> Artifact:
        command = """
        SELECT ID, QUIZ_ID, META_TYPE, FILE_TYPE, PATH
        FROM ARTIFACT
        WHERE
        """
        index = 1
        for key, (sign, _) in artifact_filter.items():
            command += f" {key.upper()} {sign} ${index} AND"
            index += 1
        command = command.rstrip("AND")
        values = [value for _, value in artifact_filter.values()]
        record = await self._connection.fetchrow(command, *values)
        return from_dict(data_class=Artifact, data=dict(record.items()))

    async def insert(self, artifact: Artifact) -> Artifact:
        command = """
        INSERT INTO ARTIFACT(QUIZ_ID, META_TYPE, FILE_TYPE, PATH)
        SELECT $1, $2, $3, $4
        RETURNING ID;
        """
        id = await self._connection.fetchval(command, artifact.quiz_id, artifact.meta_type, artifact.file_type, artifact.path)
        return await self.fetch_one_by_filter({"id": ("=", id)})

    async def update(self, id: int, artifact: dict[str, any]) -> Artifact:
        command = "UPDATE ARTIFACT SET"

        index = 1
        for key in artifact.keys():
            command += f" {key.upper()} = ${index},"
            index += 1
        command = command.rstrip(",")

        command += f"""
        WHERE ID = ${index};
        """
        _ = await self._connection.execute(command, *artifact.values(), id)
        return await self.fetch_one_by_filter({"id": ("=", id)})
