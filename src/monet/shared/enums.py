# Standard Libraries
from enum import Enum
from typing import Any, Generator


class EnumChoices(Enum):

    @classmethod
    def choices(cls) -> Generator[tuple[Any, Any]]:
        return ((elem.value, elem.name) for elem in cls)


class DomainEventSourceEnum(EnumChoices):
    ADMIN = "ADMIN"
    API = "API"
    CMD = "CMD"


class DomainEventTopicEnum(EnumChoices):
    QUIZ_CREATED = "QUIZ_CREATED"
