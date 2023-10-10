import openai


class OpenAIHandler:
    def __init__(self, temperature: float, presence_penalty: float):
        self._temperature = temperature
        self._presence_penalty = presence_penalty

    def process(self, content: str) -> list[str]:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=content,
            temperature=self._temperature,
            max_tokens=4000,
            # max_tokens=2048,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=self._presence_penalty
        )
        return [choice["text"] for choice in response["choices"]]
