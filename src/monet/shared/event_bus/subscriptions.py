# Own Libraries
from src.monet.shared.event_bus.event_bus import DomainEventBusFactory

sync_event_notification = DomainEventBusFactory.sync()

async_event_notification = DomainEventBusFactory.async_()
