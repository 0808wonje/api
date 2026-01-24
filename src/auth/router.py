from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from .service import AuthService
from .schemas import UserLoginInput, TokenResponse
from .dependencies import get_auth_service
from ..core.database import get_db


router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

@router.post("/login", response_model=TokenResponse)
def login(
    data: UserLoginInput,
    service: AuthService = Depends(get_auth_service),
    db: Session = Depends(get_db)):
    return service.procede_login(db, data)


@router.post("/token")
def swagger_ui_login(
    form: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(get_auth_service),
    db: Session = Depends(get_db)):
    data = UserLoginInput(user_id=form.username, password=form.password)
    return service.procede_login(db, data) 

