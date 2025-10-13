from typing import Annotated
from fastapi import APIRouter, Depends

from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from database.database import get_db_session
from models.user import User, UserLogin
from models.request import AppRequest
from services.authentication import get_current_user, initial_seeding, login_user

api_router = APIRouter(prefix='/api')

db_session_depends = Annotated[AsyncSession, Depends(get_db_session)]

current_user = Annotated[User, Depends(get_current_user)]

@api_router.post('/seed')
async def seeding(db_session: db_session_depends):
    result = await initial_seeding(db_session=db_session)
    return result


@api_router.post('/login')
async def login(db_session: db_session_depends, form: UserLogin) -> JSONResponse:
    [user, token] = await login_user(form=form, db_session=db_session)
    response = JSONResponse(content={"user": user})
    response.set_cookie(key='access_token', value=token, httponly=True, secure=False, samesite='none')
    return response


@api_router.get('/me')
async def me(user: current_user):
   return user
