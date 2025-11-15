# Standard Libraries
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

# Own Libraries
from src.monet.shared.enums import (
    AuditLogActionEnum,
    AuditLogObjectTypeEnum,
    DomainEventSourceEnum,
)


@dataclass(frozen=True)
class RegisterAuditLogUseCaseDTO:
    object_id: str
    obj_repr: str
    object_type: AuditLogObjectTypeEnum
    created_at: Optional[datetime] = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    created_by_id: Optional[int] = None
    source: DomainEventSourceEnum = DomainEventSourceEnum.ADMIN
    action: AuditLogActionEnum = AuditLogActionEnum.ADDITION
