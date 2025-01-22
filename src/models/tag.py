from typing import Any, Dict

from src.models.base import BaseModel


class Tag(BaseModel):
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Tag):
            return False
        return self.id == other.id and self.name == other.name

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Tag":
        return cls(id=data["id"], name=data["name"])
