from src.user.repository import UserRepository
from src.user.schemas import UserCreate, UpdateUsername, DeleteUser
from sqlalchemy.orm import Session
from src.user.exceptions import UserNotFoundException, DuplicateUsernameException, IncorrectPasswordException
from src.core.security.hashing import hash_password, verify_password

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def create_user(self, db: Session, data: UserCreate):
        try:
            is_exist = self.repo.is_username_exist(db, data.username)
            if is_exist:
                raise DuplicateUsernameException()
            else:
                values = data.model_dump()
                values['password_hash'] = hash_password(values['password_hash'])
                user = self.repo.persist_user(db, values)
                db.commit()
                db.refresh(user)
                return user
        except Exception:
            db.rollback()
            raise

    def get_user(self, db: Session, data: str):
        try:
            user = self.repo.fetch_user_by_username(db, data)
            if user:
                return user
            else:
                raise UserNotFoundException()
        except Exception:
            raise

    def modify_name(self, db: Session, data: UpdateUsername):
        try:
            is_exist = self.repo.is_username_exist(db, data.cur_name)
            if not is_exist:
                raise UserNotFoundException()
            stored_password = self.repo.fetch_user_by_username(db, data.cur_name).password_hash
            is_verified = verify_password(data.password, stored_password)
            if not is_verified:
                raise IncorrectPasswordException()
            user = self.repo.update_username(db, data.cur_name, data.after_name)
            db.commit()
            db.refresh(user)
            return user
        except Exception:
            db.rollback()
            raise

    def delete_user(self, db: Session, data: DeleteUser) -> bool:
        try:
            is_exist = self.repo.is_username_exist(db, data.username)
            if is_exist:
                self.repo.delete_user(db, data.username)
                db.commit()
                return True
            else:
                raise UserNotFoundException()
        except Exception:
            db.rollback()
            raise