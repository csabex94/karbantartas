from typing import Annotated
from fastapi import Depends, Cookie
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from ..database.schemas import UserSchema
from ..models.user import User, UserLogin
from ..utils.exception_handler import CustomExceptionHandler
from ..utils.security import SecurityUtils
from ..utils.jwt import Jwt



async def initial_seeding(db_session: AsyncSession):
    password = SecurityUtils.password_hash("Arterimpex2017")
    csaba = UserSchema(
        email="nagy.csaba@arterimpex.ro", 
        name="Nagy Csaba",
        password=password
    )
    zsombi = UserSchema(
        email="sajgo.zsombor@arterimpex.ro", 
        name="Sajgo Zsombor",
        password=password
    )
    db_session.add(csaba)
    db_session.add(zsombi)
    await db_session.commit()
    await db_session.refresh(csaba)
    await db_session.refresh(zsombi)
    return [
        User(**csaba.model_dump()),
        User(**zsombi.model_dump())
    ]


async def login_user(form: UserLogin, db_session: AsyncSession) -> list:
    query = await db_session.scalars(select(UserSchema).where(UserSchema.email == form.email))
    user: UserSchema | None = query.first()

    if user is None:
        raise CustomExceptionHandler("not_found", "User not found", 404)
    
    attempt = SecurityUtils.password_check(form.password, user.password)

    if attempt == False:
        raise CustomExceptionHandler("wrong_password", "Wrong password", 400)

    user_json = user.model_dump()
    token = Jwt.generate_token(user_json)
    return [user_json, token]
    

def get_current_user(access_token: Annotated[str | None, Cookie()]) -> User:
    if access_token is None:
        raise CustomExceptionHandler("unauthenticated", "Unauthenticated", 403)
    jwt_model = Jwt.verify_token(token=access_token)
    return jwt_model.user