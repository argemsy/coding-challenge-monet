# Standard Libraries
import asyncio
import logging
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Any, Awaitable, Callable, TypeAlias

# Own Libraries
from src.monet.shared.enums import DomainEventTopicEnum
from src.monet.shared.event_bus.domain_event import DomainEvent

logger = logging.getLogger(__name__)

SyncHandlerType: TypeAlias = Callable[[DomainEvent], None]
AsyncHandlerType: TypeAlias = Callable[[DomainEvent], Awaitable[None]]


class EventBus(ABC):
    """
    Abstract base class defining the contract for all Event Bus
    implementations.
    """

    def __init__(self) -> None:
        """Initializes the handler dictionary and class name for logging."""
        self._cls_name = self.__class__.__name__
        self._handlers: dict[DomainEventTopicEnum, list[Any]] = defaultdict(
            list
        )

    @abstractmethod
    def register(self, topic: DomainEventTopicEnum, handler: Any):
        """Registers a handler for a specific topic."""
        pass

    @abstractmethod
    def publish(self, topic: DomainEventTopicEnum, event: DomainEvent):
        pass


class SyncDomainEventBus(EventBus):
    """Concrete implementation for synchronous event processing."""

    def __init__(self) -> None:
        super().__init__()
        self._handlers: dict[DomainEventTopicEnum, list[SyncHandlerType]] = (
            defaultdict(list)
        )

    def register(self, topic: DomainEventTopicEnum, handler: SyncHandlerType):
        """Registers a synchronous handler, preventing duplicates."""

        if handler not in self._handlers[topic]:
            self._handlers[topic].append(handler)

    def publish(self, topic: DomainEventTopicEnum, event: DomainEvent):
        """
        Executes registered handlers sequentially, isolating and logging
        failures.
        """

        log_tag = f"{self._cls_name} publish"
        handlers: list[SyncHandlerType] = self._handlers.get(topic, [])
        if not handlers:
            raise ValueError(
                f"Topic {topic.value!r} is not related to any handler"
            )

        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                handler_name = (
                    handler.__name__
                    if hasattr(handler, "__name__")
                    else str(handler)
                )
                topic_name = topic.name
                logger.error(
                    f"***{log_tag}*** InternalError in {handler_name}, "
                    f"Topic: {topic_name}. Error: {e!r}",
                    exc_info=True,
                )
        logger.debug(
            f"***{log_tag}*** Concluded processing of all handlers for "
            f"topic {topic.name!r}."
        )


class AsyncDomainEventBus(EventBus):
    """
    Concrete implementation for asynchronous event processing using
    concurrency.
    """

    def __init__(self):
        super().__init__()
        self._handlers: dict[DomainEventTopicEnum, list[AsyncHandlerType]] = (
            defaultdict(list)
        )

    def register(self, topic: DomainEventTopicEnum, handler: AsyncHandlerType):
        """Registers an asynchronous handler, preventing duplicates."""

        if handler not in self._handlers[topic]:
            self._handlers[topic].append(handler)

    async def publish(self, topic: DomainEventTopicEnum, event: DomainEvent):
        """
        Executes registered handlers concurrently, isolating and logging
        failures.
        """

        log_tag = f"{self._cls_name} publish"
        handlers: list[AsyncHandlerType] = self._handlers.get(topic, [])
        if not handlers:
            raise ValueError(
                f"Topic {topic.value!r} is not related to any handler"
            )

        tasks = [handler(event) for handler in handlers]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        topic_name = topic.name

        for i, result in enumerate(results):
            if isinstance(result, Exception):
                handler = handlers[i]
                handler_name = (
                    handler.__name__
                    if hasattr(handler, "__name__")
                    else str(handler)
                )

                logger.error(
                    f"***{log_tag}*** InternalError in concurrent handler "
                    f"{handler_name!r}, Topic: {topic_name!r}. "
                    f"Error: {result!r}.",
                    exc_info=True,
                )

        logger.debug(
            f"***{log_tag}*** Concluded processing of all handlers for "
            f"topic {topic_name!r}."
        )


class DomainEventBusFactory:
    """
    A factory class to provide decoupled access to specific Event Bus
    implementations.
    """

    @staticmethod
    def sync():
        """Returns a synchronous event bus instance."""
        return SyncDomainEventBus()

    @staticmethod
    def async_():
        """Returns an asynchronous event bus instance."""
        return AsyncDomainEventBus()
