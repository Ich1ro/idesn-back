from clients.replicate_client import DiffusionClient
from data.data_lake_client import DataLakeClient
from models.DTOs.generate_dto import GenerateDto
from data.unit_of_work import UnitOfWork
from models.artifact import Artifact
from models.DTOs.delegated_download_dto import DelegatedDownload


class ImageService:
    def __init__(self, uof: UnitOfWork, diffusion_client: DiffusionClient, dl_client: DataLakeClient) -> None:
        self._uof = uof
        self._diffusion_client = diffusion_client
        self._dl_client = dl_client

    async def generate_image(self, dto: GenerateDto) -> DelegatedDownload:
        artifact = Artifact(
            id=None,
            quiz_id=None,
            meta_type="background",
            file_type="image/png",
            path=""
        )
        image_url = self._diffusion_client.generate(dto.description)[0]
        async with self._uof:
            async with await self._uof.begin():
                artifact = await self._uof.artifacts.insert(artifact)
                artifact = await self._uof.artifacts.update(artifact.id, {"path": f"/{artifact.id}/image.png"})
                await self._dl_client.copy(image_url, artifact.path)
                sas_url = self._dl_client.get_sas_access(artifact.path)
                return DelegatedDownload(url=sas_url)
