import uuid
from uuid import UUID, uuid3

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

# Base class for User model
class UserBase(SQLModel):
    name: str = Field(default=None, unique=False, max_length=255)
    email: str = Field(default=None, unique=True, max_length=255)
    phone_number: str = Field(default=None, max_length=20)
    is_active: bool = Field(default=True, nullable=False)

# Database representation of user
class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    uuid: UUID = Field(default=None, nullable=False)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)

# GET representation of user
class UserPublic(UserBase):
    email: str
    uuid: UUID

# CREATE representation of user
class UserCreate(UserBase):
    pass

# UPDATE user
class UserUpdate(UserBase):
    name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    is_active: Optional[bool] = None

