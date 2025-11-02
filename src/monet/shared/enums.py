# Standard Libraries
from enum import Enum


class EnumChoice(Enum):
    @classmethod
    def choices(cls):
        return tuple((obj.name, obj.value) for obj in cls)


class TestApprovalPercentEnum(EnumChoice):
    PERCENT_50 = "PERCENT_50"
    PERCENT_60 = "PERCENT_60"
    PERCENT_70 = "PERCENT_70"
    PERCENT_80 = "PERCENT_80"
    PERCENT_90 = "PERCENT_90"
    PERCENT_100 = "PERCENT_100"


class QuestionTypeEnum(EnumChoice):
    QUESTION_SINGLE = "QUESTION_SINGLE"
    QUESTION_MULTIPLE = "QUESTION_MULTIPLE"


class AuditLogActionEnum(EnumChoice):
    ADDITION = "ADDITION"
    CHANGE = "CHANGE"
    DELETION = "DELETION"


class AuditLogObjectTypeEnum(EnumChoice):
    STUDENT = "STUDENT"
    TEST = "TEST"
    QUESTION = "QUESTION"
    ANSWER = "ANSWER"
    FORM_STUDENT_QUESTION = "FORM_STUDENT_QUESTION"
    STUDENT_ANSWER_CHOICE = "STUDENT_ANSWER_CHOICE"


class AuditLogSourceEnum(EnumChoice):
    API = "API"
    CMD_COMMAND = "CMD_COMMAND"
    ADMIN = "ADMIN"
