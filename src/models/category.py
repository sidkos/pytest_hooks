from typing import Any, Dict

from src.models.base import BaseModel


class Category(BaseModel):
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Category):
            return False
        return self.id == other.id and self.name == other.name

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Category":
        return cls(id=data["id"], name=data["name"])
