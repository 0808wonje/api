from src.user.service import UserService
from src.user.repository import UserRepository


def get_user_service():
    return UserService(UserRepository())