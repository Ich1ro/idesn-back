from asyncpg import connection


class Repository:
    _connection: connection.Connection

    def __init__(self, connection: connection.Connection) -> None:
        self._connection = connection
