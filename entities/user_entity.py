from sqlalchemy import Column, String, Enum as SQLAEnum, DateTime, Boolean
from sqlalchemy.orm import declarative_base
from enums.role_enum import RoleEnum
from datetime import datetime

Base = declarative_base()

class UserEntity(Base):
    __tablename__ = "users"

    email = Column(String, primary_key=True, index=True)
    role = Column(SQLAEnum(RoleEnum), nullable=False)
    username = Column(String, nullable=False, index=True)
    avatar = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    email_verified = Column(Boolean, default=False)
    verification_token = Column(String, nullable=True)
    token_expiration = Column(DateTime, nullable=True)

    def __init__(self, email: str, hashed_password: str, role: RoleEnum = None, username: str = None, avatar: str = None, email_verified: bool = False, verification_token: str = None, token_expiration: datetime = None):
        self.email = email
        self.hashed_password = hashed_password
        self.role = role
        self.username = username
        self.avatar = avatar
        self.email_verified = email_verified
        self.verification_token = verification_token
        self.token_expiration = token_expiration

    def __eq__(self, other):
        if isinstance(other, UserEntity):
            return self.email == other.email
        return False

    def __str__(self):
        return f"UserEntity(email='{self.email}', role='{self.role}', username='{self.username}', avatar='{self.avatar}', email_verified='{self.email_verified}')"
