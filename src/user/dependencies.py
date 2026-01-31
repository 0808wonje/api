from .service import UserService
from .repository import UserRepository
from ..core.database import get_db
from ..core.dependencies import Redis, get_redis
from fastapi import Depends
from sqlalchemy.orm import Session



def get_user_service(
        db: Session = Depends(get_db),
        redis: Redis = Depends(get_redis)) -> UserService:
        return UserService(UserRepository(db), redis)
