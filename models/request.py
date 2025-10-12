from typing import Optional
from fastapi import Request

from models.jwt import JwtModel

class AppRequest(Request):
    jwt: Optional[JwtModel]