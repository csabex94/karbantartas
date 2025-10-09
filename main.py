from fastapi import FastAPI, Request, Response
from fastapi.concurrency import asynccontextmanager
from fastapi.responses import JSONResponse

from database.database import sessionmanager
from database.schemas import migrate
from utils.config import Settings, get_settings
from utils.security import init_security_utils
from utils.exception_handler import CustomExceptionHandler

settings: Settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_security_utils(settings.api_key_secret)
    await migrate(sessionmanager._engine)
    yield
    if sessionmanager._engine is not None:
        await sessionmanager.close()


app = FastAPI(lifespan=lifespan)

@app.exception_handler(CustomExceptionHandler)
async def custom_exception_handler(request: Request, exception: CustomExceptionHandler):
    return JSONResponse(status_code=exception.status_code, content=exception.content)

@app.middleware("http")
async def add_security_headers(request, call_next):
    response: Response = await call_next(request)
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response

@app.get('/')
def root():
    return {"OK": True}