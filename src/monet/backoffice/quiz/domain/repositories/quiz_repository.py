# Standard Libraries
from abc import ABC, abstractmethod
from typing import Iterable, Optional

# Own Libraries
from src.monet.backoffice.quiz.domain.entities.quiz_entity import EntityQuiz
from src.monet.shared.criteria import Criteria
from src.monet.shared.repository import (
    EntityT,
    ModelT,
    RepositoryInterface,
)


class QuizRepository(RepositoryInterface[ModelT, EntityT], ABC):

    @abstractmethod
    def get_object(self, criteria: Criteria) -> Optional[EntityQuiz]:
        pass

    @abstractmethod
    def get_objects(self, criteria: Criteria) -> Iterable[EntityQuiz]:
        pass

    @abstractmethod
    def save(self, entity: EntityQuiz) -> EntityQuiz:
        pass
