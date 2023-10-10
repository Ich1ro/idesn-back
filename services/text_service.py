from clients.description_generator import DescriptionGenerator
from models.DTOs.generate_dto import GenerateDto
from data.unit_of_work import UnitOfWork
from models.artifact_variable import ArtifactVariable


class TextService:
    def __init__(self, uof: UnitOfWork, description_generator: DescriptionGenerator) -> None:
        self._uof = uof
        self._description_generator = description_generator

    async def generate_text(self, dto: GenerateDto) -> str:
        text = self._description_generator.process(dto.description)
        artifact_variable = ArtifactVariable(
            id=None,
            template_id=dto.template_id,
            quiz_id=dto.quiz_id,
            input=dto.description,
            name=dto.variable,
            value=text
        )

        async with self._uof:
            async with await self._uof.begin():
                artifact_variable = await self._uof.artifact_variables.insert(artifact_variable)
                return text
