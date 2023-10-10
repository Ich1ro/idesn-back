from dataclasses import dataclass, field


@dataclass
class QuizQuestion:
    question_id: int | None
    variable: str | None
    type: str
    question: str | None
    description: str | None
    id: int | None = None
    questions: "list[QuizQuestion]" = field(default_factory=list)
