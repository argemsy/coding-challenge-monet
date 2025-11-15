# Third-party Libraries
from django.db import models

# Own Libraries
from src.monet.shared.models import AuditModel, SoftDeleteModel


class AnswerModel(AuditModel, SoftDeleteModel):
    question = models.ForeignKey(
        "QuestionModel", on_delete=models.PROTECT, related_name="answer_set"
    )
    text = models.CharField(max_length=255)
    is_correct_answer = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text} IsCorrect [{self.is_correct_answer}]"

    class Meta:
        db_table = "answer"
