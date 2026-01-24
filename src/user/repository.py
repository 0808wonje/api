from sqlalchemy.orm import Session
from datetime import datetime
from .models import Users


class UserRepository:

    def persist_user(self, db: Session, values: dict) -> Users: 
        user = Users(**values)
        db.add(user)
        return user
    
    def fetch_user_by_username(self, db: Session, username: str) -> Users:
        user = db.query(Users).filter(Users.username == username).one_or_none()
        return user

    def update_username(self, db: Session, cur_name: str, after_name: str) -> Users:
        user = db.query(Users).filter(Users.username == cur_name).one_or_none()
        user.username = after_name
        user.updated_at = datetime.now()
        return user
    
    def delete_user(self, db: Session, username: str) -> None:
        user = db.query(Users).filter(Users.username == username).one_or_none()
        db.delete(user)

    def is_username_exist(self, db: Session, username: str):
        is_exist = db.query(db.query(Users).filter(Users.username == username).exists()).scalar()
        return is_exist