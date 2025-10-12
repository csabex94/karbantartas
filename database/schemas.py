from typing import Any, Optional
from pydantic import computed_field, model_serializer
from sqlalchemy import Column
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy.dialects.mysql import LONGTEXT, JSON
from sqlalchemy.ext.asyncio import AsyncEngine
from datetime import datetime

from utils.security import SecurityUtils

class UserSchema(SQLModel, table=True):
    __tablename__="users"
    id: Optional[int] = Field(default=None, primary_key=True)
    email: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    password: Optional[str] = Field(default=None)


    @model_serializer
    def ser_model(self) -> dict[str, Any]:
        return {
            "id": SecurityUtils.hashid_encode(self.id),
            "email": self.email,
            "name": self.name
        }


class DepartmentSchema(SQLModel, table=True):
    __tablename__="departmets"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(default=None)
    uid: Optional[str] = Field(default=None)


class StoreSchema(SQLModel, table=True):
    __tablename__="stores"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(default=None)
    city: Optional[str] = Field(default=None)
    address: Optional[str] = Field(default=None)
    uid: Optional[str] = Field(default=None)



async def migrate(engine: AsyncEngine):
    async with engine.connect() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)