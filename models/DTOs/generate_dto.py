from dataclasses import dataclass


@dataclass
class GenerateDto:
    description: str
    variable: str
    template_id: int
