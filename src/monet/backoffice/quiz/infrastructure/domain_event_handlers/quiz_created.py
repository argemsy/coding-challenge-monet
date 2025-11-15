# Own Libraries
from src.monet.backoffice.audit_log.application.register_audit_log_dto import (
    RegisterAuditLogUseCaseDTO,
)
from src.monet.backoffice.audit_log.infrastructure import (
    DjangoORMAuditLogRepositoryImpl,
)
from src.monet.backoffice.quiz.domain.entities.quiz_entity import EntityQuiz
from src.monet.shared.enums import (
    AuditLogObjectTypeEnum,
    DomainEventSourceEnum,
)
from src.monet.shared.event_bus.domain_event import DomainEvent


async def audit_log_register_quiz_created_handler(
    event: DomainEvent[EntityQuiz],
):
    # Own Libraries
    from src.monet.backoffice.audit_log.application import (
        RegisterAuditLogUseCase,
    )

    repository = DjangoORMAuditLogRepositoryImpl()
    use_case = RegisterAuditLogUseCase(repository=repository)

    entity: EntityQuiz = event.event
    source: DomainEventSourceEnum = event.source

    dto = RegisterAuditLogUseCaseDTO(
        object_id=str(entity.pk),
        obj_repr=entity.name,
        object_type=AuditLogObjectTypeEnum.QUIZ,
        created_at=event.created_at,
        source=source,
        created_by_id=event.owner_id,
    )
    await use_case.execute(dto=dto)
