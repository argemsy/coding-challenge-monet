import logging

import pytest

from src.monet.backoffice.audit_log.domain.audit_log_entity import \
    EntityAuditLog
from src.monet.backoffice.audit_log.infrastructure import \
    DjangoORMAuditLogRepositoryImpl
from src.monet.backoffice.quiz.application.dtos.create_quiz_dto import \
    CreateQuizUseCaseDTO
from src.monet.backoffice.quiz.application.use_cases import \
    CreateQuizUseCase
from src.monet.backoffice.quiz.infrastructure.reposotories import \
    DjangoORMQuizRepositoryImpl
from src.monet.shared.enums import AuditLogActionEnum, AuditLogObjectTypeEnum, \
    DomainEventSourceEnum

logging.basicConfig(level=logging.DEBUG)


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_create_quiz_use_case():

    repository = DjangoORMQuizRepositoryImpl()
    use_case = CreateQuizUseCase(repository=repository)
    use_case.user_id = 1818

    dto = CreateQuizUseCaseDTO(
        name="Fake Quiz", description="..:: Description ::..",
    )
    for _ in range(1000):
        resp = await use_case.execute(dto=dto)
        assert resp

        assert resp.pk
        assert resp.name == dto.name
        assert resp.description == dto.description

        await use_case.publish_event(event=resp)

@pytest.mark.django_db
async def test_audit_log_repo_create_in_bulk():

    repository = DjangoORMAuditLogRepositoryImpl()

    entities = [
        EntityAuditLog(
            object_id=str(index+1),
            obj_repr=f"QuizFake#{index+1}",
            object_type=AuditLogObjectTypeEnum.QUIZ,
            created_by_id=1,
            source=DomainEventSourceEnum.ADMIN,
            action=AuditLogActionEnum.ADDITION
        )
        for index in range(10000)
    ]

    resp = await repository.save(entities=entities, batch_size=2500)
    assert resp
    assert isinstance(resp, list)
    print(f"{resp.pop(-1).to_create()=}")
