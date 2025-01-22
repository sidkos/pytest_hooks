import uuid

import pytest

from src.clients.petstore_client.petstore_client import PetStoreClient
from src.helpers.tool_box import random_id, random_string
from src.models.category import Category
from src.models.pet import Pet
from src.models.tag import Tag


@pytest.fixture(scope="function", name="random_pet")
def generate_pet(random_tag: Tag, random_category: Category, status: str = "available") -> Pet:
    return Pet(
        id=random_id(),
        name=f"pet_{random_string()}",
        category=random_category,
        photo_urls=["https://example.com/buddy1.jpg", "https://example.com/buddy2.jpg"],
        tags=[random_tag],
        status=status,
    )


@pytest.fixture(scope="function", name="random_tag")
def generate_tag() -> Tag:
    return Tag(
        id=random_id(),
        name=str(uuid.uuid4()),
    )


@pytest.fixture(scope="function", name="random_category")
def generate_category() -> Category:
    return Category(id=random_id(), name=str(uuid.uuid4()))


@pytest.fixture(scope="session", name="pet_store_client")
def pet_store_client() -> PetStoreClient:
    return PetStoreClient()
