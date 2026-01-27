from fastapi import FastAPI
from contextlib import asynccontextmanager
from .user.router import router as user_router
from .auth.router import router as auth_router
from .core.router import router as core_router
from .user.models import Base
from .core.database import engine
from .core.exception_handler import user_not_found_handler, duplicate_username_handler, incorrect_password_handler
from .user.exceptions import UserNotFoundException, DuplicateUsernameException, IncorrectPasswordException
from .core.redis_config import init_redis, close_redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔵 App is starting up...")
    Base.metadata.create_all(bind=engine)
    init_redis()
    yield
    close_redis()
    print("🔴 App is shutting down gracefully...")

app = FastAPI(lifespan=lifespan)

    
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(core_router)

app.add_exception_handler(UserNotFoundException, user_not_found_handler)
app.add_exception_handler(DuplicateUsernameException, duplicate_username_handler)
app.add_exception_handler(IncorrectPasswordException, incorrect_password_handler)
