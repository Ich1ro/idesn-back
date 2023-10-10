from dataclasses import dataclass
from typing import Optional


@dataclass
class Quiz:
    id: Optional[int]
    template_id: int
