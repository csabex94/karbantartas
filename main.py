from fastapi import FastAPI, Request, Response
from fastapi.concurrency import asynccontextmanager
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from models.request import AppRequest
from routers.api_router import api_router
from database.database import sessionmanager
from database.schemas import migrate
from utils.config import Settings, get_settings
from utils.security import init_security_utils
from utils.jwt import Jwt, init_jwt
from utils.exception_handler import CustomExceptionHandler

settings: Settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_security_utils(settings.api_key_secret)
    init_jwt(settings.jwt_rsa_private_key)
    await migrate(sessionmanager._engine)
    yield
    if sessionmanager._engine is not None:
        await sessionmanager.close()

origins = ["http://localhost:5173"]

app = FastAPI(lifespan=lifespan)

app.mount("/frontend", StaticFiles(directory="frontend/dist"), name="frontend")

templates = Jinja2Templates(directory='frontend/dist')

@app.get('/')
async def app_template(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.exception_handler(CustomExceptionHandler)
async def custom_exception_handler(request: Request, exception: CustomExceptionHandler):
    return JSONResponse(status_code=exception.status_code, content=exception.content)

@app.middleware("http")
async def check_auth_cookie(request: AppRequest, call_next):
    token: str | None = request.cookies.get('access_token', None)
    print(token)
    if token != False:
        jwt_model = Jwt.verify_token(token)
        request.jwt = jwt_model
        return await call_next(request)
    
    return await call_next(request)

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response


app.include_router(router=api_router)