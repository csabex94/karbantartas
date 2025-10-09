from typing import Any, Optional
from pydantic import computed_field
from sqlalchemy import Column
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy.dialects.mysql import LONGTEXT, JSON
from sqlalchemy.ext.asyncio import AsyncEngine
from datetime import datetime

class UserSchema(SQLModel, table=True):
    __tablename__="users"
    id: Optional[int] = Field(default=None, primary_key=True)
    email: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    password: Optional[str] = Field(default=None)
    api_key: Optional["ApiKeySchema"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "joined"})


class ApiKeySchema(SQLModel, table=True):
    __tablename__="apikeys"
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_key: str = Field(nullable=False, unique=True)
    encrypted_key: Optional[str] = Field(default=None)
    user_id: Optional[int] = Field(foreign_key="users.id", default=None)
    user: Optional["UserSchema"] = Relationship(back_populates="api_key", sa_relationship_kwargs={"lazy": "joined"})


async def migrate(engine: AsyncEngine):
    async with engine.connect() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)