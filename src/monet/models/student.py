# Standard Libraries
import uuid

# Third-party Libraries
from django.db import models

# Own Libraries
from src.monet.shared.models import AuditModel, SoftDeleteModel
from django.contrib.auth import get_user_model


User = get_user_model()


class StudentModel(AuditModel, SoftDeleteModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student")
    nro_carnet = models.UUIDField(
        editable=False, default=uuid.uuid4, db_index=True, unique=True,
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    class Meta:
        db_table = "student"
