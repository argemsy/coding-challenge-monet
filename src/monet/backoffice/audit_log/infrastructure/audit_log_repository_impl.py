# Standard Libraries
import logging

# Third-party Libraries
from django.db import DatabaseError

# Own Libraries
from src.monet.backoffice.audit_log.domain.audit_log_entity import (
    EntityAuditLog,
)
from src.monet.backoffice.audit_log.domain.audit_log_repository import (
    AuditLogRepository,
)
from src.monet.backoffice.audit_log.domain.exceptions import (
    AuditLogRepositoryExceptionError,
    AuditLogRepositoryPersistenceExceptionError,
)
from src.monet.models import AuditLogModel
from src.monet.shared.database import async_database

logger = logging.getLogger(__name__)


class DjangoORMAuditLogRepositoryImpl(
    AuditLogRepository[AuditLogModel, EntityAuditLog]
):
    def __init__(self):
        super().__init__(model_cls=AuditLogModel, entity_cls=EntityAuditLog)

    @async_database()
    def save(
        self,
        entities: list[EntityAuditLog],
        batch_size: int = 100,
    ) -> list[EntityAuditLog]:
        log_tag = f"{self._cls_name} save"
        try:
            if not entities:
                logger.warning(f"***{log_tag}*** No entities to save")
                return []

            if batch_size <= 0:
                raise ValueError(f"Invalid batch size: {batch_size}")

            model_cls = self.get_model_cls()

            # transform entities to model instances to create
            try:
                objs = [model_cls(**entity.to_create()) for entity in entities]
            except (AttributeError, TypeError, ValueError):
                raise

            new_instances = []
            total_count = len(entities)
            _batch_size = min(batch_size, total_count)

            for start_idx in range(0, total_count, _batch_size):
                end_idx = start_idx + _batch_size
                objs_batch = objs[start_idx:end_idx]
                new_instances.extend(model_cls.objects.bulk_create(objs_batch))

            _entity = self.get_entity_cls()
            data = [
                _entity.from_db_model(instance=instance)
                for instance in new_instances
            ]
            logger.info(
                f"***{log_tag}*** AuditLogs: {len(data)} elements was saved"
            )
            return data
        except (AttributeError, TypeError, ValueError) as exp:
            logger.warning(f"***{log_tag}*** {exp!r}")
            raise AuditLogRepositoryExceptionError(str(exp)) from exp
        except DatabaseError as exp:
            logger.error(f"***{log_tag}*** {exp!r}", exc_info=True)
            raise AuditLogRepositoryPersistenceExceptionError(
                str(exp)
            ) from exp
