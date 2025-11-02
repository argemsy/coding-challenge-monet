# Third-party Libraries
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import Q

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
    created_by_id = models.IntegerField(db_index=True)

    class Meta:
        db_table = "question"


class SingleQuestionModel(AuditModel, SoftDeleteModel):
    question = models.ForeignKey(
        "QuestionModel", on_delete=models.PROTECT, related_name="simple_set"
    )
    text = models.CharField(max_length=50)
    correct_answer = models.IntegerField(db_index=True, blank=True, null=True)

    def __str__(self):
        return f"{self.text}"

    class Meta:
        db_table = "single_question"
        constraints = [
            models.UniqueConstraint(
                fields=["question"],
                condition=Q(is_deleted=False),
                name="unique_active_simple_question_per_question",
            )
        ]


class MultipleQuestionModel(AuditModel, SoftDeleteModel):
    question = models.ForeignKey(
        "QuestionModel", on_delete=models.PROTECT, related_name="multiple_set"
    )
    text = models.CharField(max_length=50)
    correct_answers = ArrayField(
        models.IntegerField(),
        default=list,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.text}"

    class Meta:
        db_table = "multiple_question"
