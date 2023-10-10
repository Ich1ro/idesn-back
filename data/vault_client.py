import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from models.adl_config import ADLConfig
from models.db_config import DbConfig


class VaultClient:
    _client: SecretClient

    def __init__(self) -> None:
        name = os.environ["KEY_VAULT_NAME"]
        tenants = os.environ["ADDITIONALLY_ALLOWED_TENANTS"].split(",")
        credential = DefaultAzureCredential(additionally_allowed_tenants=tenants, exclude_shared_token_cache_credential=True)
        self._client = SecretClient(vault_url=f"https://{name}.vault.azure.net", credential=credential)

    def get_db_config(self) -> DbConfig:
        url = self._client.get_secret("DbUrl").value
        name = self._client.get_secret("DbName").value
        port = self._client.get_secret("DbPort").value
        user = self._client.get_secret("DbUser").value
        password = self._client.get_secret("DbPassword").value

        return DbConfig(url, name, port, user, password)

    def get_adl_config(self) -> ADLConfig:
        access_key = self._client.get_secret("BlobAccessKey").value
        return ADLConfig(access_key)
