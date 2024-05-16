import json
import httpx

from src.external_service.schemas import PublicAPIsResponse


class Client:
    """
    This is the client to Public APIs service,
    which returns the list of APIs with public access.
    """

    # BASE_URL: str = "https://api.publicapis.org"
    # BASE_URL: str = "https://publicapis.dev/"
    BASE_URL: str = "https://raw.githubusercontent.com/naimjeem/Public-APIs/master/json"

    @property
    def client(self):
        return httpx.AsyncClient(base_url=self.BASE_URL, timeout=10.0)

    async def get_public_apis(self) -> PublicAPIsResponse:
        async with self.client as client:
            response = await client.get("/entries.json")
            data = response.json()

            return PublicAPIsResponse.model_validate_json(
                json.dumps(dict(count=10, entries=data["Development"]))
            )
