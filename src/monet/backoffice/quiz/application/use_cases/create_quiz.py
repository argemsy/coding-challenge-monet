# Standard Libraries
import logging
from typing import Any, Optional

# Own Libraries
from src.monet.backoffice.quiz.application.dtos.create_quiz_dto import (
    CreateQuizUseCaseDTO,
)
from src.monet.backoffice.quiz.domain.entities.quiz_entity import EntityQuiz
from src.monet.backoffice.quiz.domain.repositories.quiz_repository import (
    QuizRepository,
)
from src.monet.shared.enums import DomainEventSourceEnum, DomainEventTopicEnum
from src.monet.shared.event_bus.domain_event import DomainEvent
from src.monet.shared.event_bus.event_bus import EventBus
from src.monet.shared.event_bus.subscriptions import async_event_notification
from src.monet.shared.exceptions import (
    ServiceExceptionError,
    UseCaseExceptionError,
)
from src.monet.shared.repository import EntityT, ModelT
from src.monet.shared.use_case import UseCase

logger = logging.getLogger(__name__)


class CreateQuizUseCase(UseCase):
    def __init__(
        self,
        repository: QuizRepository[ModelT, EntityT],
        event_bus: Optional[EventBus] = None,
    ):
        super().__init__()
        self._repository = repository
        self._event_bus = event_bus or async_event_notification

    async def publish_event(
        self,
        event: EntityQuiz,
        metadata: Optional[dict[str, Any]] = None,
    ) -> None:
        log_tag = f"{self.__class__.__name__} publish event"
        logger.debug(f"***{log_tag}*** Start")

        domain_event: DomainEvent[EntityQuiz] = DomainEvent(
            source=DomainEventSourceEnum.PRIVATE_API,
            owner_id=self.user_id,
            event=event,
            metadata=metadata or {},
        )

        await self._event_bus.publish(
            topic=DomainEventTopicEnum.QUIZ_CREATED,
            event=domain_event,
        )
        logger.info(f"***{log_tag}*** Success!!")
        return None  # type: ignore

    async def execute(self, dto: CreateQuizUseCaseDTO) -> EntityQuiz:
        try:
            entity = EntityQuiz(
                name=dto.name,
                description=dto.description,
                created_by_id=self.user_id,
            )
            return await self._repository.save(entity=entity)  # type: ignore
        except ServiceExceptionError as exp:
            raise UseCaseExceptionError(str(exp)) from exp
