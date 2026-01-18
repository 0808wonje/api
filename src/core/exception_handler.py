from fastapi import Request
from fastapi.responses import JSONResponse
from src.user.exceptions import UserNotFoundException, DuplicateUsernameException, IncorrectPasswordException

def user_not_found_handler(request: Request, exc: UserNotFoundException):
    return JSONResponse(
        status_code=404,
        content={"detail": "User not found"}
    )

def duplicate_username_handler(request: Request, exc: DuplicateUsernameException):
    return JSONResponse(
        status_code=409,
        content={"detail": "Username already exists"}
    )

def incorrect_password_handler(request: Request, exc: IncorrectPasswordException):
    return JSONResponse(
        status_code=404,
        content={"detail": "Incorrect password"}
    )
