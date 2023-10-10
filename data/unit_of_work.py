from functools import cached_property
from asyncpg import connect, connection, transaction
from data.repositories.quiz_repository import QuizRepository
from data.repositories.quiz_question_repository import QuizQuestionRepository
from data.vault_client import VaultClient
from data.repositories.artifact_repository import ArtifactRepository
from data.repositories.artifact_variable_repository import ArtifactVariableRepository


class UnitOfWork:
    _connection: connection.Connection

    def __init__(self, vault_client: VaultClient) -> None:
        self._vault_client = vault_client

    @cached_property
    def artifacts(self) -> ArtifactRepository:
        return ArtifactRepository(self._connection)
    
    @cached_property
    def artifact_variables(self) -> ArtifactVariableRepository:
        return ArtifactVariableRepository(self._connection)
    
    @cached_property
    def quizzes(self) -> QuizRepository:
        return QuizRepository(self._connection)
    
    @cached_property
    def quiz_questions(self) -> QuizQuestionRepository:
        return QuizQuestionRepository(self._connection)

    async def begin(self) -> transaction.Transaction:
        return self._connection.transaction()

    async def _connect(self) -> None:
        config = self._vault_client.get_db_config()
        self._connection = await connect(
            host=config.url,
            port=config.port,
            user=config.user,
            database=config.name,
            password=config.password
        )

    async def _close(self) -> None:
        if self._connection and not self._connection.is_closed():
            await self._connection.close()

    async def __aenter__(self):
        await self._connect()
        return self

    async def __aexit__(self, *args, **kwargs):
        await self._close()
