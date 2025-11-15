# Third-party Libraries
from django.db import models

# Own Libraries
from src.monet.shared.models import AuditModel, SoftDeleteModel


class FormStudentTestModel(AuditModel, SoftDeleteModel):
    test = models.ForeignKey("TestModel", on_delete=models.PROTECT)
    student = models.ForeignKey("StudentModel", on_delete=models.PROTECT)
    correct_answers = models.SmallIntegerField(default=0)
    wrong_answers = models.SmallIntegerField(default=0)
    is_approved = models.BooleanField(default=False, db_index=True)
    is_closed = models.BooleanField(default=False, db_index=True)

    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name}"

    class Meta:
        db_table = "form_student_test"
