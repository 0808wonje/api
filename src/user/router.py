from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from .schemas import *
from .dependencies import UserService, get_user_service
from ..auth.dependencies import get_current_user_id
from ..core.limiter import rate_limit


router = APIRouter(
    prefix='/user',
    tags=['User']
)

@router.post("/join", response_model=UserCreateResponse)
def join(
    data: UserCreate, 
    service: UserService = Depends(get_user_service)):
    user = service.create_user(data)
    return user

@router.get("/find", response_model=FindUserResponse, name='find_user')
async def find_user(
    service: UserService = Depends(get_user_service),
    user_id: str =  Depends(get_current_user_id),
    _: None = Depends(rate_limit)):
    user = await service.get_user_from_cache_first(user_id)
    return user

@router.post("/change", response_model=UpdateUsernameResponse)
async def change_username(
    after_username: str,
    service: UserService = Depends(get_user_service),
    user_id: str =  Depends(get_current_user_id)):
    user = await service.modify_name(user_id, after_username)
    return user

@router.post("/quit")
async def quit(
    service: UserService = Depends(get_user_service),
    user_id: str =  Depends(get_current_user_id)):
    await service.delete_user(user_id)
    return DeleteUserResponse(msg='Your account is deleted')
    # return RedirectResponse(url="/", status_code=302)