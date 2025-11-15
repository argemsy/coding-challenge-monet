# Own Libraries
from src.monet.backoffice.quiz.infrastructure.domain_event_handlers import (
    audit_log_register_quiz_created_handler,
)
from src.monet.shared.enums import DomainEventTopicEnum
from src.monet.shared.event_bus.event_bus import DomainEventBusFactory

# -- SYNC NOTIFICATIONS -- #

sync_event_notification = DomainEventBusFactory.sync()

# -- ASYNC NOTIFICATIONS -- #

async_event_notification = DomainEventBusFactory.async_()

async_event_notification.register(
    topic=DomainEventTopicEnum.QUIZ_CREATED,
    handler=audit_log_register_quiz_created_handler,
)
