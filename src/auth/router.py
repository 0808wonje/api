from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from .service import AuthService
from .schemas import UserLoginInput, TokenResponse
from .dependencies import get_auth_service


router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

@router.post("/login", response_model=TokenResponse)
def login(
    data: UserLoginInput,
    service: AuthService = Depends(get_auth_service)):
    return service.procede_login(service, data)


@router.post("/token")
def swagger_ui_login(
    form: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(get_auth_service)):
    data = UserLoginInput(username=form.username, password=form.password)
    return service.procede_login(data) 

