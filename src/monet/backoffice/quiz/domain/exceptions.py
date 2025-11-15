# Own Libraries
from src.monet.shared.exceptions import (
    DomainExceptionError,
    PersistenceExceptionError,
    ServiceExceptionError,
)


class QuizModelExceptionError(ServiceExceptionError):
    pass


class QuizRepositoryPersistenceExceptionError(PersistenceExceptionError):
    pass


class DTOValidationExceptionError(DomainExceptionError):
    pass
