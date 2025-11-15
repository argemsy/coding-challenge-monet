# Standard Libraries
from dataclasses import dataclass
from typing import Optional

# Own Libraries
from src.monet.backoffice.quiz.domain.exceptions import (
    DTOValidationExceptionError,
)


@dataclass(frozen=True)
class CreateQuizUseCaseDTO:
    name: str
    description: Optional[str] = None

    MAX_NAME_LENGTH = 40

    def __post_init__(self):
        if len(self.name) > self.MAX_NAME_LENGTH:
            raise DTOValidationExceptionError(
                f"The 'name' field cannot exceed {self.MAX_NAME_LENGTH} "
                f"characters. Current length: {len(self.name)}"
            )

        if not isinstance(self.name, str) or not self.name.strip():
            raise DTOValidationExceptionError(
                "The 'name' field cannot be empty."
            )
