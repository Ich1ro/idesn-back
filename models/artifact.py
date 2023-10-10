from dataclasses import dataclass
from typing import Optional


@dataclass
class Artifact:
    id: Optional[int]
    quiz_id: Optional[int]
    meta_type: str
    file_type: str
    path: str
