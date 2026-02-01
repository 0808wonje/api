from sqlalchemy.orm import Session
from datetime import datetime
from .models import Users, SocialAccount


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, values: dict) -> Users: 
        user = Users(**values)
        self.db.add(user)
        self.db.flush()
        return user
    
    def add_social_user(self, user: Users, values: dict) -> SocialAccount:
        social_user = SocialAccount(**values)
        user.social_accounts.append(social_user)
        self.db.add(user)
        self.db.flush()
        return user
    
    def get_by_id(self, user_id: int) -> Users | None:
        user = self.db.query(Users).filter(Users.id == user_id).one_or_none()
        return user
    
    def get_by_username(self, username: str) -> Users | None:
        user = self.db.query(Users).filter(Users.username == username).one_or_none()
        return user
    
    def get_social_user_by_provider_id(
            self, 
            provider:str,
            provider_id: str) -> Users | None:
        user = self.db.query(SocialAccount).filter(
            SocialAccount.provider == provider, SocialAccount.provider_id == provider_id
            ).one_or_none()
        return user
    
    def delete(self, user_id: int) -> None:
        user = self.db.query(Users).filter(Users.id == user_id).first()
        self.db.delete(user)

    def is_username_exist(self, username: str):
        is_exist = self.db.query(self.db.query(Users).filter(Users.username == username).exists()).scalar()
        return is_exist