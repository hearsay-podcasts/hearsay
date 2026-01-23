import uuid
from datetime import datetime

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


# Podcast models
class PodcastBase(SQLModel):
    title: str = Field(max_length=500)
    author: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None)
    cover_url: str | None = Field(default=None, max_length=2000)
    feed_url: str | None = Field(default=None, unique=True, index=True, max_length=2000)
    is_featured: bool = Field(default=False, index=True)
    # Listen Notes fields
    listenotes_id: str | None = Field(default=None, unique=True, index=True, max_length=255)
    publisher: str | None = Field(default=None, max_length=500)
    total_episodes: int | None = Field(default=None)
    listen_score: int | None = Field(default=None)
    genre_ids: str | None = Field(default=None, max_length=500)
    listenotes_url: str | None = Field(default=None, max_length=2000)
    # iTunes artwork fields
    itunes_id: str | None = Field(default=None, max_length=255)
    cover_url_sm: str | None = Field(default=None, max_length=2000)
    cover_url_md: str | None = Field(default=None, max_length=2000)
    cover_url_lg: str | None = Field(default=None, max_length=2000)


class Podcast(PodcastBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class PodcastPublic(PodcastBase):
    id: uuid.UUID


class PodcastList(SQLModel):
    podcasts: list[PodcastPublic]
    count: int


# Cache metadata for tracking API data freshness
class CacheMetadata(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    cache_key: str = Field(unique=True, index=True, max_length=255)
    last_fetched_at: datetime = Field(default_factory=datetime.utcnow)
