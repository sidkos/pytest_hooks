from typing import Any, Dict, List, Optional

from src.models.base import BaseModel
from src.models.category import Category
from src.models.tag import Tag


class Pet(BaseModel):
    def __init__(
        self,
        id: int,
        name: str,
        category: Optional[Category] = None,
        photo_urls: Optional[List[str]] = None,
        tags: Optional[List[Tag]] = None,
        status: Optional[str] = None,
    ):
        super().__init__(id, name)
        self._category = category
        self._photo_urls = photo_urls or []
        self._tags = tags or []
        self._status = status

    @property
    def category(self) -> Optional[Category]:
        return self._category

    @category.setter
    def category(self, value: Optional[Category]) -> None:
        self._category = value

    @property
    def photo_urls(self) -> List[str]:
        return self._photo_urls

    @photo_urls.setter
    def photo_urls(self, value: List[str]) -> None:
        self._photo_urls = value

    @property
    def tags(self) -> List[Tag]:
        return self._tags

    @tags.setter
    def tags(self, value: List[Tag]) -> None:
        self._tags = value

    @property
    def status(self) -> Optional[str]:
        return self._status

    @status.setter
    def status(self, value: Optional[str]) -> None:
        self._status = value

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Pet":
        return cls(
            id=data["id"],
            name=data["name"],
            category=Category.from_dict(data["category"]) if "category" in data else None,
            photo_urls=data.get("photoUrls", []),
            tags=[Tag.from_dict(tag) for tag in data.get("tags", [])],
            status=data.get("status"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category.to_dict() if self.category else None,
            "photoUrls": self.photo_urls,
            "tags": [tag.to_dict() for tag in self.tags],
            "status": self.status,
        }

    def __repr__(self) -> str:
        return (
            f"Pet(id={self.id}, name='{self.name}', category={self.category}, "
            f"photo_urls={self.photo_urls}, tags={self.tags}, status='{self.status}')"
        )
