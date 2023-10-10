from typing import final
from clients.openai_handler import OpenAIHandler


ACTION_DESCRIPTION: final = "Generate description for such case"


class DescriptionGenerator(OpenAIHandler):
    def __init__(self):
        super().__init__(temperature=0.5, presence_penalty=0.0)
        self._template = f"{ACTION_DESCRIPTION}:\n\n" + "{content}"

    def process(self, content: str) -> list[str]:
        return super().process(self._template.format(content=content))[0]
