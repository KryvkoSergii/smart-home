from fastapi import APIRouter, Depends, HTTPException, status
from schemas.user_schemas import UserResponse, UserRegistrationRequest
from schemas.shared_schemas import ErrorResponse
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_db
from services.users import UserService
from logger import logger
from services.accounts import AccountService
from logger.logger import build_logger

router = APIRouter(prefix="/users", tags=["users"])
logger = build_logger("user", "DEBUG")

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        409: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def register_new_user(
    user_data: UserRegistrationRequest,
    db: AsyncSession = Depends(get_db),
):
    user_service = UserService(logger, db)
    account_service = AccountService(logger, db)
    
    email_user = await user_service.get_user_by_email(user_data.email)
    if email_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with such email already exists",
        )

    username_user = await user_service.get_user_by_username(user_data.username)
    if username_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with such username already exists",
        )
    
    account = await account_service.create_account()
    new_user = await user_service.register_new_user(user_data, account)

    return new_user