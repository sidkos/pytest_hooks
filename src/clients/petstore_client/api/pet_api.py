from typing import Any, Optional, cast

import requests

from src.models.pet import Pet


class PetAPI:
    def __init__(self, base_url: str, headers: dict[str, str]) -> None:
        self.base_url = base_url
        self.headers = headers

    def _request(
        self,
        method: str,
        endpoint: str,
        *,
        params: Optional[dict[str, Any]] = None,
        json: Optional[dict[str, Any]] = None,
        files: Optional[dict[str, Any]] = None,
    ) -> Any:
        url = f"{self.base_url}{endpoint}"
        response = requests.request(method, url, headers=self.headers, params=params, json=json, files=files)
        response.raise_for_status()
        return response.json() if response.content else None

    def get_pet_by_id(self, pet_id: int) -> Pet:
        data = self._request("GET", f"/pet/{pet_id}")
        return Pet.from_dict(data)

    def find_pets_by_status(self, status: str) -> list[Pet]:
        data = self._request("GET", "/pet/findByStatus", params={"status": status})
        return [Pet.from_dict(pet) for pet in cast(list[dict[str, Any]], data)]

    def add_pet(self, pet_obj: Pet) -> Pet:
        data = self._request("POST", "/pet", json=pet_obj.to_dict())
        return Pet.from_dict(data)

    def update_pet(self, pet_obj: Pet) -> Pet:
        data = self._request("PUT", "/pet", json=pet_obj.to_dict())
        return Pet.from_dict(data)

    def delete_pet_by_id(self, pet_id: int, return_response: bool = False) -> Optional[dict[str, Any]]:
        response = self._request("DELETE", f"/pet/{pet_id}")
        return response if return_response else None

    def upload_pet_image(self, pet_id: int, image_path: str) -> dict[str, Any]:
        with open(image_path, "rb") as image_file:
            return cast(dict[str, Any], self._request("POST", f"/pet/{pet_id}/uploadImage", files={"file": image_file}))
