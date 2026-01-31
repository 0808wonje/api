from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from .service import AuthService
from .schemas import UserLoginInput, TokenResponse, SocialLoginInput
from .dependencies import get_auth_service, get_current_user_id, oauth2_scheme
from ..core.security.jwt import decode_token


router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

@router.post("/login", response_model=TokenResponse)
def local_login(
    data: UserLoginInput,
    service: AuthService = Depends(get_auth_service)):
    return service.procede_local_login(data)

@router.post("/logout")
async def logout(
    service: AuthService = Depends(get_auth_service),
    user_id = Depends(get_current_user_id),
    token: str = Depends(oauth2_scheme)):
    jwt = decode_token(token)
    return await service.procede_logout(jwt)


@router.post("/token")
def swagger_ui_login(
    form: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(get_auth_service)):
    data = UserLoginInput(username=form.username, password=form.password)
    return service.procede_local_login(data) 

@router.get("/{provider}/login")
async def social_login(provider:str, request: Request):
    if provider not in request.app.state.oauth._clients:
        raise
    client = getattr(request.app.state.oauth, provider)
    redirect_uri = str(request.url_for("social_callback", provider=provider))
    return await client.authorize_redirect(request, redirect_uri)

@router.get("/{provider}/callback", name="social_callback")
async def social_callback(
    provider:str,
    request: Request,
    service: AuthService = Depends(get_auth_service)):
    client = getattr(request.app.state.oauth, provider)
    token = await client.authorize_access_token(request)
    if provider == 'google':
        pass
    userinfo = token['userinfo']
    data = SocialLoginInput(
        provider=provider,
        provider_id=userinfo['sub'],
        social_email=userinfo['email'])
    return service.procede_social_login(data)
    

