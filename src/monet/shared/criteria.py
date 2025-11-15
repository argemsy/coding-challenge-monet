# Standard Libraries
from abc import ABC
from dataclasses import dataclass, field
from typing import Any, Optional

# Third-party Libraries
from django.db.models import Q


@dataclass()
class PaginationField:
    page: int = field(default=1)
    page_size: int = field(default=8)

    def validate(self) -> None:
        if self.page < 1:
            raise ValueError("Page must be greater than 0")
        if self.page_size < 1:
            raise ValueError("Page size must be greater than 0")


@dataclass
class Criteria(ABC):
    q_filter: Any
    pagination: PaginationField = field(default_factory=PaginationField)
    order_by: Optional[list[str]] = field(default=None)

    def get_offset(self) -> int:
        """Compute offset"""
        return (self.pagination.page - 1) * self.pagination.page_size


@dataclass
class DjangoCriteria(Criteria):
    q_filter: Q = field(default_factory=Q)
