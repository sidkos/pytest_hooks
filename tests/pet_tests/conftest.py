from typing import Generator, Tuple

import pytest

from src.clients.petstore_client.petstore_client import PetStoreClient
from src.models.pet import Pet


@pytest.fixture(scope="function", name="add_random_pet")
def add_random_pet(
    pet_store_client: PetStoreClient, random_pet: Pet
) -> Generator[Tuple[PetStoreClient, Pet], None, None]:
    pet_store_client.pet_api.add_pet(random_pet)
    yield pet_store_client, random_pet
    pet_store_client.pet_api.delete_pet_by_id(random_pet.id)
