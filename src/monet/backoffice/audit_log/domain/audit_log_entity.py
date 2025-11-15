# Standard Libraries
from datetime import datetime, timezone
from typing import Any, Optional, Union

# Own Libraries
from src.monet.shared.enums import (
    AuditLogActionEnum,
    AuditLogObjectTypeEnum,
    DomainEventSourceEnum,
    normalize_enum,
)


class EntityAuditLog:
    def __init__(
        self,
        object_id: Optional[str] = None,
        obj_repr: Optional[str] = None,
        object_type: Union[str, AuditLogObjectTypeEnum, None] = None,
        created_at: Optional[datetime] = None,
        pk: Optional[int] = None,
        created_by_id: Optional[int] = None,
        source: Union[str, DomainEventSourceEnum, None] = None,
        action: Union[str, AuditLogActionEnum, None] = None,
    ):
        self.object_id = object_id
        self.obj_repr = obj_repr
        self.object_type = normalize_enum(object_type, AuditLogObjectTypeEnum)
        self.created_at = created_at or datetime.now(timezone.utc)
        self.pk = pk
        self.created_by_id = created_by_id
        self.source = normalize_enum(source, DomainEventSourceEnum)
        self.action = normalize_enum(action, AuditLogActionEnum)

    @classmethod
    def from_db_model(cls, instance):
        return cls(
            pk=instance.id,
            created_by_id=instance.created_by_id,
            object_id=instance.object_id,
            obj_repr=instance.obj_repr,
            object_type=instance.object_type,
            created_at=instance.created_at,
            source=instance.source,
            action=instance.action,
        )

    def to_create(self) -> dict[str, Any]:
        to_create_dict = {
            "object_id": self.object_id,
            "obj_repr": self.obj_repr,
            "object_type": self.object_type_str,
            "created_at": self.created_at,
            "source": self.source_str,
            "action": self.action_str,
        }
        is_command = (
            self.source == DomainEventSourceEnum.CMD_COMMAND
            or self.source_str == DomainEventSourceEnum.CMD_COMMAND.value
        )
        if not is_command:
            to_create_dict["created_by_id"] = self.created_by_id

        if missing_fields := {
            field for field, value in to_create_dict.items() if value is None
        }:
            errors = ", ".join(missing_fields)
            raise ValueError(f"Missing required fields: {errors}.")
        return to_create_dict

    @property
    def object_type_str(self) -> str:
        if isinstance(self.object_type, AuditLogObjectTypeEnum):
            return self.object_type.value
        raise ValueError(f"Invalid object_type: {self.object_type}")

    @property
    def source_str(self) -> str:
        if isinstance(self.source, DomainEventSourceEnum):
            return self.source.value
        raise ValueError(f"Invalid source: {self.source}")

    @property
    def action_str(self) -> str:
        if isinstance(self.action, AuditLogActionEnum):
            return self.action.value
        raise ValueError(f"Invalid action: {self.action}")
