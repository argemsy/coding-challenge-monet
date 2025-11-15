# Standard Libraries
import logging
from typing import Iterable, Optional, Type

# Third-party Libraries
from django.db import DatabaseError

# Own Libraries
from src.monet.backoffice.quiz.domain.entities import EntityQuiz
from src.monet.backoffice.quiz.domain.exceptions import (
    QuizRepositoryPersistenceExceptionError,
)
from src.monet.backoffice.quiz.domain.repositories import (
    QuizRepository,
)
from src.monet.models.test import TestModel
from src.monet.shared.criteria import Criteria
from src.monet.shared.database import async_database

# Local Folders Libraries
from .helpers import QuizRepositoryHelper

logger = logging.getLogger(__name__)


class DjangoORMQuizRepositoryImpl(QuizRepository[TestModel, EntityQuiz]):

    def __init__(
        self,
        helper: Optional[Type[QuizRepositoryHelper]] = None,
    ) -> None:
        super().__init__(model_cls=TestModel, entity_cls=EntityQuiz)
        self._helper = helper or QuizRepositoryHelper

    @async_database()
    def get_object(self, criteria: Criteria) -> Optional[EntityQuiz]:
        model = self.get_model_cls()

        qs = model.objects.filter(criteria.q_filter)

        if not (instance := qs.first()):
            return None

        entity = self.get_entity_cls()
        return entity.from_db_model(instance=instance)

    @async_database()
    def get_objects(self, criteria: Criteria) -> Iterable[EntityQuiz]:
        model = self.get_model_cls()

        qs = model.objects.filter(criteria.q_filter)
        entity = self.get_entity_cls()

        return [entity.from_db_model(instance=instance) for instance in qs]

    @async_database()
    def save(self, entity: EntityQuiz) -> EntityQuiz:
        log_tag = f"{self._cls_name} save"
        try:
            model_cls = self.get_model_cls()
            common_params = {
                "entity": entity,
                "model_cls": model_cls,
            }

            if entity.pk:
                instance = self._helper.update_instance(**common_params)
            else:
                instance = self._helper.create_instance(**common_params)

            entity = self.get_entity_cls()
            return entity.from_db_model(instance=instance)
        except DatabaseError as exp:
            logger.error(f"***{log_tag}*** {exp!r}", exc_info=True)
            raise QuizRepositoryPersistenceExceptionError(str(exp)) from exp
