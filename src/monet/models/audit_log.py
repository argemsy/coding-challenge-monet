# Standard Libraries
from typing import Optional

# Third-party Libraries
from django.db import models
from pydantic import BaseModel, Field

# Own Libraries
from src.monet.shared.enums import (
    AuditLogActionEnum,
    AuditLogObjectTypeEnum,
    DomainEventSourceEnum,
)


class AuditLogMetadataField(BaseModel):
    version: int = 1
    change_message: str = Field(default="")
    update_fields: list[str] = Field(default_factory=list)
    previous_value: Optional[dict] = Field(default_factory=dict)
    new_value: Optional[dict] = Field(default_factory=dict)


def metadata_default():
    metadata = AuditLogMetadataField()
    return metadata.model_dump()


class AuditLogModel(models.Model):
    created_by_id = models.IntegerField(db_index=True, blank=True, null=True)
    action = models.CharField(
        max_length=15,
        choices=AuditLogActionEnum.choices(),
        db_index=True,
    )
    object_id = models.CharField(max_length=50, db_index=True)
    object_type = models.CharField(
        max_length=50,
        choices=AuditLogObjectTypeEnum.choices(),
        db_index=True,
    )
    obj_repr = models.CharField(max_length=100)
    metadata = models.JSONField(
        blank=True, null=True, default=metadata_default
    )
    source = models.CharField(
        max_length=50,
        choices=DomainEventSourceEnum.choices(),
        default=DomainEventSourceEnum.ADMIN.value,
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f"[{self.object_id}] {self.object_type}. "

    class Meta:
        db_table = "audit_log"
