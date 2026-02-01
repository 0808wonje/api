from __future__ import annotations
from typing import Protocol, TYPE_CHECKING


if TYPE_CHECKING:
    from src.user.models import Users, SocialAccount

class UserQueryPort(Protocol):
    def add(self, values: dict) -> Users:
        ...

    def add_social_user(self, user, values: dict) -> SocialAccount:
        ...

    def get_by_id(self, user_id: int) -> Users | None:
        ...

    def get_by_username(self, username: str) -> Users:
        ...

    def get_social_user_by_provider_id(self, 
            provider:str,
            provider_id: str) -> Users:
        ...