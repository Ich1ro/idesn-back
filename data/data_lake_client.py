import os
import aiohttp
from datetime import datetime, timedelta
from typing import AsyncIterator
from azure.storage.filedatalake.aio import DataLakeServiceClient
from azure.storage.filedatalake import ResourceTypes, AccountSasPermissions, generate_account_sas
from azure.identity.aio import DefaultAzureCredential
from data.vault_client import VaultClient


class DataLakeClient:
    _vault_client: VaultClient
    _container_name: str
    _client: DataLakeServiceClient

    def __init__(self, vault_client: VaultClient, container_name: str) -> None:
        self._vault_client = vault_client
        self._container_name = container_name
        name = os.environ["ADL_NAME"]
        tenants = os.environ["ADDITIONALLY_ALLOWED_TENANTS"].split(",")
        credential = DefaultAzureCredential(additionally_allowed_tenants=tenants, exclude_shared_token_cache_credential=True)
        self._client = DataLakeServiceClient(account_url=f"https://{name}.dfs.core.windows.net/", credential=credential)

    async def copy(self, from_url: str, to_path: str) -> None:
        file_system = self._client.get_file_system_client(self._container_name)
        file = await file_system.create_file(to_path)
        async with aiohttp.ClientSession() as session:
            async with session.get(from_url) as resp:
                content = await resp.read()
                await file.upload_data(content, overwrite=True)

    async def download_stream(self, path: str) -> AsyncIterator[bytes]:
        file = self._client.get_file_client(self._container_name, path)
        stream = await file.download_file()
        return stream.chunks()

    def get_sas_access(self, blob: str) -> str:
        adl_config = self._vault_client.get_adl_config()
        sas_token = generate_account_sas(
            self._client.account_name,
            account_key=adl_config.access_key,
            resource_types=ResourceTypes(object=True),
            permission=AccountSasPermissions(read=True),
            expiry=datetime.utcnow() + timedelta(hours=1)
        )
        blob = blob.strip("/")
        return f"https://{self._client.account_name}.dfs.core.windows.net/{self._container_name}/{blob}?{sas_token}"
