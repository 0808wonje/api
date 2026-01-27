from __future__ import annotations
from typing import Protocol, TYPE_CHECKING


if TYPE_CHECKING:
    from src.user.models import Users

class UserReader(Protocol):
    def fetch_user_by_username(self, db, username: str) -> Users:
        ...

