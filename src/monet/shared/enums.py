# Standard Libraries
from enum import Enum
from typing import Any, Generator, Optional, Type, TypeVar

E = TypeVar("E", bound=Enum)


class EnumChoices(Enum):

    @classmethod
    def choices(cls: Type[E]) -> Generator[tuple[Any, str], None, None]:
        return ((elem.value, elem.name) for elem in cls)


def normalize_enum(value: Any, enum_class: type[E]) -> Optional[E]:
    if value is None:
        return None
    if isinstance(value, enum_class):
        return value
    if isinstance(value, str):
        try:
            return enum_class[value]
        except KeyError as e:
            raise ValueError(f"Invalid {enum_class.__name__}: {value}") from e
    raise TypeError(
        f"Expected str or {enum_class.__name__}, got {type(value)}"
    )


class DomainEventSourceEnum(EnumChoices):
    PUBLIC_API = "PUBLIC_API"
    PRIVATE_API = "PRIVATE_API"
    CMD_COMMAND = "CMD_COMMAND"
    ADMIN = "ADMIN"


class DomainEventTopicEnum(EnumChoices):
    QUIZ_CREATED = "QUIZ_CREATED"


class AuditLogObjectTypeEnum(EnumChoices):
    STUDENT = "STUDENT"
    QUIZ = "QUIZ"
    QUESTION = "QUESTION"
    ANSWER = "ANSWER"
    FORM_STUDENT_QUESTION = "FORM_STUDENT_QUESTION"
    STUDENT_ANSWER_CHOICE = "STUDENT_ANSWER_CHOICE"


class AuditLogActionEnum(EnumChoices):
    ADDITION = "ADDITION"
    CHANGE = "CHANGE"
    DELETION = "DELETION"


class TestApprovalPercentEnum(EnumChoices):
    PERCENT_50 = "PERCENT_50"
    PERCENT_60 = "PERCENT_60"
    PERCENT_70 = "PERCENT_70"
    PERCENT_80 = "PERCENT_80"
    PERCENT_90 = "PERCENT_90"
    PERCENT_100 = "PERCENT_100"


class QuestionTypeEnum(EnumChoices):
    QUESTION_SINGLE = "QUESTION_SINGLE"
    QUESTION_MULTIPLE = "QUESTION_MULTIPLE"
