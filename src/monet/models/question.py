# Third-party Libraries
from django.contrib.postgres.fields import ArrayField
from django.db import models

# Own Libraries
from src.monet.shared.enums import QuestionTypeEnum
from src.monet.shared.models import AuditModel, SoftDeleteModel


class QuestionModel(AuditModel, SoftDeleteModel):
    test = models.ForeignKey(
        "TestModel", on_delete=models.PROTECT, related_name="question_set"
    )
    question_type = models.CharField(
        db_index=True,
        max_length=50,
        choices=QuestionTypeEnum.choices(),
        default=QuestionTypeEnum.QUESTION_SINGLE.value,
    )
    text = models.CharField(max_length=150)
    correct_answers = ArrayField(
        models.IntegerField(),
        default=list,
        blank=True,
        null=True,
    )
    created_by_id = models.IntegerField(db_index=True)

    class Meta:
        db_table = "question"
