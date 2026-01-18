from src.core.config import *
from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.user import router
from src.user.models import Base
from src.core.database import engine
from src.core.exception_handler import user_not_found_handler, duplicate_username_handler, incorrect_password_handler
from src.user.exceptions import UserNotFoundException, DuplicateUsernameException, IncorrectPasswordException

# graceful shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔵 App is starting up...")
    Base.metadata.create_all(bind=engine)
    yield
    print("🔴 App is shutting down gracefully...")

app = FastAPI(lifespan=lifespan)
    
app.include_router(router.router, tags=['user'])

app.add_exception_handler(UserNotFoundException, user_not_found_handler)
app.add_exception_handler(DuplicateUsernameException, duplicate_username_handler)
app.add_exception_handler(IncorrectPasswordException, incorrect_password_handler)
