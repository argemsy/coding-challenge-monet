# Standard Libraries
from dataclasses import asdict

# Own Libraries
from src.monet.backoffice.audit_log.application.register_audit_log_dto import (
    RegisterAuditLogUseCaseDTO,
)
from src.monet.backoffice.audit_log.domain.audit_log_entity import (
    EntityAuditLog,
)
from src.monet.backoffice.audit_log.domain.audit_log_repository import (
    AuditLogRepository,
)
from src.monet.shared.exceptions import (
    DomainExceptionError,
    UseCaseExceptionError,
)
from src.monet.shared.repository import EntityT, ModelT
from src.monet.shared.use_case import UseCase


class RegisterAuditLogUseCase(UseCase):
    def __init__(self, repository: AuditLogRepository[ModelT, EntityT]):
        super().__init__()
        self._repository = repository

    async def execute(self, dto: RegisterAuditLogUseCaseDTO):
        try:
            entity = EntityAuditLog(**asdict(dto))
            await self._repository.save(entities=[entity])
        except UseCaseExceptionError as exp:
            raise DomainExceptionError(str(exp)) from exp
