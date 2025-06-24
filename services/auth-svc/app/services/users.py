from sqlalchemy.ext.asyncio import AsyncSession

from repository.users import UserRepository
from schemas.user_schemas import UserRegistrationRequest, UserResponse, CreateUserRequest
from repository.models import User
from hash import get_password_hash
from logging import Logger
from repository.models import Account

class UserService:

    def __init__(self, logger: Logger, db: AsyncSession):
        self.__user_repository = UserRepository(db)
        self.__logger = logger

    async def register_new_user(self, body: UserRegistrationRequest, account: Account) -> UserResponse:
        self.__logger.info(f"Registering user username: '{body.username}' email: '{body.email}'")
        user = User(
            **body.model_dump(exclude_unset=True, exclude={"password"}),
            hashed_password=get_password_hash(body.password),
            account_id=account.id
        )
        found = await self.__user_repository.create_user(user)
        return self.__transform_user_model(found)
    
    # async def create_user(self, body: CreateUserRequest) -> UserModel:
    #     self.__logger.info(f"Creating user username: '{body.username}' email: '{body.email}'")
    #     user = User(
    #         **body.model_dump(exclude_unset=True, exclude={"password"}),
    #         hashed_password=get_password_hash(str(uuid.uuid4()))  # Assuming password is not required for this operation,
    #     )
    #     found = await self.__user_repository.create_user(user)
    #     return self.__transform_user_model(found)

    async def get_user_by_username(self, username: str) -> UserResponse | None:
        found = await self.get_user_entity_by_username(username)
        return self.__transform_user_model(found)

    async def get_user_by_email(self, email: str) -> UserResponse | None:
        found = await self.get_user_entity_by_email(email)
        return self.__transform_user_model(found)
    
    def __transform_user_model(self, user: User) -> UserResponse | None:
        self.__logger.debug(f"Transforming user model: {user}")
        return UserResponse.model_validate(user) if user else None
