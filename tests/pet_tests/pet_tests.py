from typing import Any, Tuple

import pytest

from src.clients.petstore_client.petstore_client import PetStoreClient
from src.helpers.tool_box import random_id, random_string
from src.models.category import Category
from src.models.pet import Pet
from src.models.tag import Tag


@pytest.mark.pet
@pytest.mark.update_pet
@pytest.mark.parametrize(
    "attribute, updated_value",
    [
        pytest.param("name", random_string(), marks=pytest.mark.sanity),
        ("category", Category(id=random_id(), name=random_string())),
        ("photo_urls", [f"https://example.com/{random_string()}.jpg"]),
        ("tags", [Tag(id=random_id(), name=random_string())]),
        ("status", "sold"),
    ],
    ids=[
        "Update name",
        "Update category",
        "Update photo URLs",
        "Update tags",
        "Update status",
    ],
)
def test_update_existing_pet(add_random_pet: Tuple[PetStoreClient, Pet], attribute: str, updated_value: Any) -> None:
    """
    Test updating an existing pet's attributes directly using objects or values.

    Steps:
    1. Use the `add_random_pet` fixture to create a random pet and add it to the pet store.
    2. Dynamically update the specified attribute of the pet using the given updated value.
    3. Perform an API request to update the pet in the pet store.
    4. Fetch the updated pet from the API using its ID.
    5. Assert that the updated attribute matches the expected value.
    """
    # Step 1:
    pet_store_client, random_pet = add_random_pet

    # Step 2:
    setattr(random_pet, attribute, updated_value)

    # Step 3:
    pet_store_client.pet_api.update_pet(random_pet)

    # Step 4:
    retrieved_pet = pet_store_client.pet_api.get_pet_by_id(random_pet.id)

    # Step 5:
    assert getattr(retrieved_pet, attribute) == updated_value, (
        f"Attribute '{attribute}' did not update correctly. "
        f"Expected: {updated_value}, Found: {getattr(retrieved_pet, attribute)}"
    )
