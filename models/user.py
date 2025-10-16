from typing import Any
from pydantic import BaseModel, model_serializer

from ..utils.security import SecurityUtils

class User(BaseModel):
    id: str
    email: str
    name: str
    

class UserLogin(BaseModel):
    email: str
    password: str


