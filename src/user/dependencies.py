from src.user.service import UserService
from src.user.repository import UserRepository
from src.auth.service import AuthService


def get_user_service() -> UserService:
    return UserService(UserRepository())