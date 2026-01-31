from __future__ import annotations
from typing import Protocol, TYPE_CHECKING


if TYPE_CHECKING:
    from src.user.models import Users, SocialAccount

class UserQueryPort(Protocol):
    def persist_user(self, values: dict) -> Users:
        ...

    def persist_social_user(self, user, values: dict) -> SocialAccount:
        ...

    def fetch_user_by_username(self, username: str) -> Users:
        ...

    def fetch_social_user_by_provider_id(self, 
            provider:str,
            provider_id: str) -> Users:
        ...