"""Page template reader module"""

from re import findall, DOTALL
from models.page_template import PageTemplate
from data.data_lake_client import DataLakeClient
from data.unit_of_work import UnitOfWork


class PageTemplateReader:
    """Reads page templates"""
    _dl_client: DataLakeClient

    def __init__(self, uof: UnitOfWork, dl_client: DataLakeClient) -> None:
        self._uof = uof
        self._dl_client = dl_client

    async def get(self, id: int) -> PageTemplate:
        """Returns HTML template file by path"""
        async with self._uof:
            artifact = await self._uof.artifacts.fetch_one_by_filter(artifact_filter={
                "id": ("=", id),
                "meta_type": ("=", "TEMPLATE"),
            })

            template_stream = await self._dl_client.download_stream(f"/{artifact.path}/template.html")
            style_stream = await self._dl_client.download_stream(f"/{artifact.path}/style.css")
            script_stream = await self._dl_client.download_stream(f"/{artifact.path}/script.js")

            template_chunks = [chunk.decode("utf-8") async for chunk in template_stream]
            template = "".join(template_chunks)
            css_chunks = [chunk.decode("utf-8") async for chunk in style_stream]
            css = "".join(css_chunks)
            js_chunks = [chunk.decode("utf-8") async for chunk in script_stream]
            js = "".join(js_chunks)

            variables = findall("\{(\w+)\}", template, DOTALL)

            return PageTemplate(html=template, js=js, css=css, elements=variables)
