from datetime import datetime
from uuid import UUID

from sqlmodel import Field, SQLModel


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
    name: str | None = None
    email: str | None = None
    phone_number: str | None = None
    is_active: bool | None = None

