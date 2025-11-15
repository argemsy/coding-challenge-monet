class DomainExceptionError(Exception):
    pass


class UseCaseExceptionError(DomainExceptionError):
    pass


class ServiceExceptionError(UseCaseExceptionError):
    pass


class PersistenceExceptionError(ServiceExceptionError):
    pass
