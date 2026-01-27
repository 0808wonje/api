from sqlalchemy.orm import Session
from redis import Redis
import json
from .repository import UserRepository
from .models import Users
from .schemas import UserCreate, UpdateUsername, DeleteUser
from .exceptions import UserNotFoundException, DuplicateUsernameException
from src.core.security.hashing import hash_password
from ..core.constants import REDIS_TTL_SECONDS



class UserService:
    def __init__(self, db: Session, repo: UserRepository, redis: Redis):
        self.db = db
        self.repo = repo
        self.redis = redis

    def create_user(self, data: UserCreate):
        try:
            is_exist = self.repo.is_username_exist(self.db, data.username)
            if is_exist:
                raise DuplicateUsernameException()
            else:
                values = data.model_dump()
                values['password_hash'] = hash_password(values['password_hash'])
                user = self.repo.persist_user(self.db, values)
                self.db.commit()
                self.db.refresh(user)
                return user
        except Exception:
            self.db.rollback()
            raise
    
    def get_user_from_db(self, db: Session, data: str) -> Users:
        try:
            user = self.repo.fetch_user_by_username(db, data)
            if user:
                return user
            else:
                raise UserNotFoundException()
        except Exception:
            raise

    def get_user_from_cache_first(self, user_id: int) -> dict:
        try:
            cached = self.redis.get(user_id)
            if cached:
                return json.loads(cached)
            user = self.repo.fetch_user_by_id(self.db, user_id)
            if user:
                user_dict = json.dumps({
                    "id" : user.id,
                    "username" : user.username
                })
                self.redis.set(user_id, user_dict, ex=REDIS_TTL_SECONDS)
                return json.loads(user_dict)
            else:
                raise UserNotFoundException()
        except Exception:
            raise

    def modify_name(self, user_id: int, after_name: str):
        try:
            user = self.repo.update_username(self.db, user_id, after_name)
            self.redis.delete(user_id)
            self.db.commit()
            self.db.refresh(user)
            return user
        except Exception:
            self.db.rollback()
            raise

    def delete_user(self, user_id) -> bool:
        try:
            self.repo.delete_user(self.db, user_id)
            self.redis.delete(user_id)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise