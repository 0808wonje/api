from .service import UserService
from .repository import UserRepository


def get_user_service() -> UserService:
    return UserService(UserRepository())