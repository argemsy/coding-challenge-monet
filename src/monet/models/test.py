# Third-party Libraries
from django.db import models

# Own Libraries
from src.monet.shared.enums import TestApprovalPercentEnum
from src.monet.shared.models import AuditModel, SoftDeleteModel


class TestModel(AuditModel, SoftDeleteModel):
    name = models.CharField(max_length=40)
    description = models.TextField(blank=True, null=True)
    created_by_id = models.IntegerField(db_index=True)

    def __str__(self):
        return f"Test {self.name}"

    class Meta:
        db_table = "test"


class TestSettingsModel(AuditModel, SoftDeleteModel):
    test = models.OneToOneField(
        "TestModel", on_delete=models.PROTECT, related_name="settings"
    )
    total_questions = models.SmallIntegerField(default=0)
    approval_percent = models.CharField(
        max_length=30,
        choices=TestApprovalPercentEnum.choices(),
        default=TestApprovalPercentEnum.PERCENT_50.value,
        db_index=True,
    )
    has_retry = models.BooleanField(default=False)
    retry_limit = models.IntegerField(default=0)

    def __str__(self):
        return f"Settings for {self.test.name}"

    class Meta:
        db_table = "test_settings"
