# Own Libraries
from src.monet.shared.exceptions import (
    PersistenceExceptionError,
    ServiceExceptionError,
)


class AuditLogRepositoryExceptionError(ServiceExceptionError):
    pass


class AuditLogRepositoryPersistenceExceptionError(PersistenceExceptionError):
    pass
