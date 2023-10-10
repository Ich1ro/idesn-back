from dataclasses import dataclass


@dataclass
class DbConfig:
    url: str
    name: str
    port: int
    user: str
    password: str
