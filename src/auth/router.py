from fastapi import APIRouter, Depends, Request
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
    return service.procede_login(data)


@router.post("/token")
def swagger_ui_login(
    form: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(get_auth_service)):
    data = UserLoginInput(username=form.username, password=form.password)
    return service.procede_login(data) 


@router.get("/google/login")
async def google_login(request: Request):
    redirect_uri = str(request.url_for("google_callback"))
    return await request.app.state.oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/google/callback", name="google_callback")
async def google_callback(request: Request):
    token = await request.app.state.oauth.google.authorize_access_token(request)
    print('token ========= ', token)
    userinfo = await request.app.state.oauth.google.parse_id_token(request, token)
    # TODO: upsert user + issue JWT
    return userinfo

