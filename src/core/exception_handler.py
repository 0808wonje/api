from fastapi import Request
from fastapi.responses import JSONResponse
from ..user.exceptions import UserNotFoundException, DuplicateUsernameException, IncorrectPasswordException
from sqlalchemy.exc import IntegrityError


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

def integrity_error_handler(request: Request, exc: IntegrityError):
    orig = getattr(exc, 'orig', None)
    #Postgres(psycopg2)
    pgcode = getattr(orig, "pgcode", None)
    if pgcode == '23505':
        constraint = getattr(getattr(orig, "diag", None), "constraint_name", None)
        if constraint == 'uq_users_username':
            return JSONResponse(
                status_code=409,
                content={"detail": "username conflicted"},
            )
        if constraint == 'uq_users_email':
            return JSONResponse(
                status_code=409,
                content={"detail": "email conflicted"},
            )
    return JSONResponse(status_code=400, content={"detail": "Integrity error"})
