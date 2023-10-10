from dataclasses import dataclass
from typing import Optional


@dataclass
class ArtifactVariable:
    id: Optional[int]
    template_id: int
    quiz_id: Optional[int]
    input: str
    name: str
    value: str
