import pytest
from unittest.mock import AsyncMock, MagicMock

from app.services.users import UserService
from app.schemas.user_schemas import UserRegistrationRequest, UserResponse
from app.repository.models import User, Account
from pydantic import SecretStr

@pytest.fixture
def logger():
    return MagicMock()

@pytest.fixture
def db():
    return MagicMock()

@pytest.fixture
def user_repository_mock(monkeypatch):
    repo_mock = AsyncMock()
    monkeypatch.setattr("app.services.users.UserRepository", lambda db: repo_mock)
    return repo_mock

@pytest.fixture
def user_service(logger, db, user_repository_mock):
    return UserService(logger, db)

@pytest.fixture
def account():
    return Account(id="00000000-0000-0000-0000-000000000001")

@pytest.fixture
def user():
    return User(
        id="00000000-0000-0000-0000-000000000001",
        username="testuser",
        email="test@example.com",
        hashed_password="hashed",
        account_id="00000000-0000-0000-0000-000000000001",
        account=Account(id="00000000-0000-0000-0000-000000000001"),
        created_at="2023-10-01T00:00:00Z"
    )

@pytest.fixture
def registration_request():
    return UserRegistrationRequest(
        username="testuser",
        email="test@example.com",
        password=SecretStr("123456789")
    )

@pytest.mark.asyncio
async def test_register_new_user(user_service, user_repository_mock, registration_request, account, user):
    user_repository_mock.create_user.return_value = user

    result = await user_service.register_new_user(registration_request, account)
    assert isinstance(result, UserResponse)
    assert result.username == user.username
    assert result.email == user.email

@pytest.mark.asyncio
async def test_get_user_by_username(user_service, user_repository_mock, user):
    user_repository_mock.get_user_by_username.return_value = user

    result = await user_service.get_user_by_username("testuser")
    assert isinstance(result, UserResponse)
    assert result.username == user.username

@pytest.mark.asyncio
async def test_get_user_by_email(user_service, user_repository_mock, user):
    user_repository_mock.get_user_by_email.return_value = user

    result = await user_service.get_user_by_email("test@example.com")
    assert isinstance(result, UserResponse)
    assert result.email == user.email

@pytest.mark.asyncio
async def test_get_user_by_username_not_found(user_service, user_repository_mock):
    user_repository_mock.get_user_by_username.return_value = None

    result = await user_service.get_user_by_username("notfound")
    assert result is None

@pytest.mark.asyncio
async def test_get_user_by_email_not_found(user_service, user_repository_mock):
    user_repository_mock.get_user_by_email.return_value = None

    result = await user_service.get_user_by_email("notfound@example.com")
    assert result is None