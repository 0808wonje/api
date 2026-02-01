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

@router.put("/create", response_model=UserCreateResponse)
def create_user(
    data: UserCreate, 
    service: UserService = Depends(get_user_service)):
    user = service.register_user(data)
    return user

@router.get("/me", response_model=FindUserResponse, name='find_me')
async def find_me(
    service: UserService = Depends(get_user_service),
    user_id: str =  Depends(get_current_user_id),
    _: None = Depends(rate_limit)):
    user = await service.get_user_profile(user_id)
    return user

@router.patch("/me", response_model=UpdateUsernameResponse)
async def update_me(
    data: UpdateUserProfile,
    service: UserService = Depends(get_user_service),
    user_id: str =  Depends(get_current_user_id)):
    user = await service.change_profile(user_id, data)
    return user

@router.delete("/me", status_code=204)
async def delete_me(
    service: UserService = Depends(get_user_service),
    user_id: str =  Depends(get_current_user_id)):
    await service.delete_user(user_id)
    # return RedirectResponse(url="/", status_code=204)
