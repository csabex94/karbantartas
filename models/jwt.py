from typing import Optional
from pydantic import BaseModel

from models.user import User

class JwtModel(BaseModel):
    iat: Optional[int]
    exp: Optional[int]
    sub: Optional[str]
    aud: Optional[str]
    iss: Optional[str]
    scope: Optional[str]
    user: Optional[User]