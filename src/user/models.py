from __future__ import annotations
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DateTime, BigInteger, UniqueConstraint, Index, Text, ForeignKey
from datetime import datetime, timezone


class Base(DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("username", name="uq_users_username"),
        UniqueConstraint("email", name="uq_users_email"),
        Index("idx_users_email", "email"),
    )
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str | None] = mapped_column(String, nullable=True) 
    password_hash: Mapped[str] = mapped_column(String(255), nullable=True) 
    email: Mapped[str] = mapped_column(String(255), nullable=True)
    age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    social_accounts: Mapped[list[SocialAccount]] = relationship(
        back_populates="users",
        cascade="all, delete-orphan",
    )

class SocialAccount(Base):
    __tablename__ = "social_accounts"
    __table_args__ = (
        UniqueConstraint("provider", "provider_id", name="uq_social_provider_providerid"),
        UniqueConstraint("user_id", "provider", name="uq_social_user_provider"),
        Index("idx_social_provider_providerid", "provider", "provider_id"),
    )
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    #FK, This column references id of users
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    #google/kakao/naver etc..
    provider: Mapped[str] = mapped_column(String(20), nullable=False)
    #userinfo['sub']  
    provider_id: Mapped[str] = mapped_column(String(255), nullable=False) 
    social_email: Mapped[str] = mapped_column(String(255), nullable=False)

    users: Mapped[Users] = relationship(back_populates="social_accounts")


     
