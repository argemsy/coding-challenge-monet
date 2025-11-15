# Standard Libraries
from typing import Optional


class EntityQuiz:
    def __init__(
        self,
        name: str,
        pk: Optional[int] = None,
        description: Optional[str] = None,
        created_by_id: Optional[int] = None,
    ):
        self.pk = pk
        self.name = name
        self.description = description
        self.created_by_id = created_by_id

    @classmethod
    def from_db_model(cls, instance):
        return cls(
            pk=instance.id,
            name=instance.name,
            description=instance.description,
            created_by_id=instance.created_by_id,
        )
