# Third-party Libraries
from django.db import models

# Own Libraries
from src.monet.shared.models import AuditModel, SoftDeleteModel


class StudentAnswerChoiceModel(AuditModel, SoftDeleteModel):
    form = models.ForeignKey(
        "FormStudentTestModel",
        on_delete=models.DO_NOTHING,
        related_name="student_answer_set",
    )
    student = models.ForeignKey("StudentModel", on_delete=models.DO_NOTHING)
    question = models.ForeignKey("QuestionModel", on_delete=models.DO_NOTHING)
    answer = models.ForeignKey("AnswerModel", on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "student_answer_choice"
