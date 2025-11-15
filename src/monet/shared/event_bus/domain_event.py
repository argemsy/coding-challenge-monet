# Standard Libraries
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Generic, Optional, TypeVar

# Own Libraries
from src.monet.shared.enums import DomainEventSourceEnum

EntityT = TypeVar("EntityT")


@dataclass(frozen=True)
class DomainEvent(Generic[EntityT]):
    source: DomainEventSourceEnum
    owner_id: Optional[int] = field(default=None)
    event: Optional[EntityT] = field(default=None)
    events: list[EntityT] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: Optional[datetime] = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
