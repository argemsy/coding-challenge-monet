# Standard Libraries
from abc import ABC
from typing import Generic, Optional, Type, TypeVar

EntityT = TypeVar("EntityT")
ModelT = TypeVar("ModelT")


class RepositoryInterface(Generic[ModelT, EntityT], ABC):

    def __init__(
        self,
        model_cls: Optional[Type[ModelT]] = None,
        entity_cls: Optional[Type[EntityT]] = None,
    ):
        self._cls_name = self.__class__.__name__
        self.model_cls = model_cls
        self.entity_cls = entity_cls

    def get_model_cls(self) -> Type[ModelT]:
        cls_name = self.__class__.__name__
        if not self.model_cls:
            raise ValueError(f"Model not register in {cls_name}")
        return self.model_cls

    def get_entity_cls(self) -> Type[EntityT]:
        cls_name = self.__class__.__name__
        if not self.entity_cls:
            raise ValueError(f"Entity not register in {cls_name}")
        return self.entity_cls
