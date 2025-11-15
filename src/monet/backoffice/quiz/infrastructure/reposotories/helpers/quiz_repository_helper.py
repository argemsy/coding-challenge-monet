# Standard Libraries
from datetime import datetime, timezone
from typing import Type

# Own Libraries
from src.monet.backoffice.quiz.domain.entities.quiz_entity import EntityQuiz
from src.monet.backoffice.quiz.domain.exceptions import QuizModelExceptionError
from src.monet.models import TestModel


class QuizRepositoryHelper:
    @staticmethod
    def update_instance(
        entity: EntityQuiz,
        model_cls: Type[TestModel],
    ) -> TestModel:

        if not (instance := model_cls.objects.filter(pk=entity.pk).first()):
            raise QuizModelExceptionError("Test Instance not found")
        if instance.is_deleted:
            raise QuizModelExceptionError("Test previously was deleted")

        update_fields = set()

        if instance.name != entity.name:
            instance.name = entity.name
            update_fields.add("name")

        if entity.description and instance.description != entity.description:
            instance.description = entity.description
            update_fields.add("description")

        if update_fields:
            instance.updated_at = datetime.now(timezone.utc)
            update_fields.add("updated_at")
            instance.save(update_fields=list(update_fields))

        return instance

    @staticmethod
    def create_instance(
        entity: EntityQuiz,
        model_cls: Type[TestModel],
    ) -> TestModel:
        instance = model_cls(
            name=entity.name,
            description=entity.description,
            created_by_id=entity.created_by_id,
        )
        instance.save()
        return instance
