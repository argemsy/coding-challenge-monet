# Standard Libraries
from abc import ABC, abstractmethod
from typing import Any, Optional


class UseCase(ABC):

    _user_id: Optional[int] = None

    @property
    def user_id(self) -> int:
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("user_id must be a positive integer")
        self._user_id = value

    @abstractmethod
    async def execute(self, dto: Any):
        pass
