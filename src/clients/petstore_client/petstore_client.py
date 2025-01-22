from src.clients.petstore_client.api.pet_api import PetAPI


class PetStoreClient:
    def __init__(self, base_url: str = "https://petstore.swagger.io/v2", api_key: str = "special-key") -> None:
        self.base_url = base_url
        self.api_key = api_key
        self.headers: dict[str, str] = self.authenticate()
        self.pet_api = PetAPI(base_url=self.base_url, headers=self.headers)

    def authenticate(self) -> dict[str, str]:
        if not self.api_key:
            raise ValueError("API key is required for authentication.")
        return {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
