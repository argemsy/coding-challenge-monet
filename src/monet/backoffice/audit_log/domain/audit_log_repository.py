# Standard Libraries
from abc import ABC, abstractmethod

# Own Libraries
from src.monet.backoffice.audit_log.domain.audit_log_entity import (
    EntityAuditLog,
)
from src.monet.shared.repository import EntityT, ModelT, RepositoryInterface


class AuditLogRepository(RepositoryInterface[ModelT, EntityT], ABC):
    @abstractmethod
    def save(
        self,
        entities: list[EntityAuditLog],
        batch_size: int = 100,
    ) -> list[EntityAuditLog]:
        pass
