import uuid

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    full_name: str | None = Field(default=None, max_length=255)
    is_active: bool = True


# Properties to receive via API on registration
class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=128)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation (admin)
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)


# Database model
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str


# Properties to return via API
class UserPublic(UserBase):
    id: uuid.UUID


# Login request
class LoginRequest(SQLModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


# Generic message response
class Message(SQLModel):
    message: str


# Token payload
class TokenPayload(SQLModel):
    sub: str | None = None
