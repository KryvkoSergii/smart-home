import pytest
from unittest.mock import AsyncMock, MagicMock

from app.services.accounts import AccountService
from app.repository.accounts import Account
from uuid import UUID

@pytest.fixture
def logger():
    return MagicMock()

@pytest.fixture
def db():
    return MagicMock()

@pytest.fixture
def account_repository_mock(monkeypatch):
    repo_mock = AsyncMock()
    monkeypatch.setattr("app.services.accounts.AccountRepository", lambda db: repo_mock)
    return repo_mock

@pytest.fixture
def account_service(logger, db, account_repository_mock):
    return AccountService(logger, db)

@pytest.fixture
def account():
    return Account(id="00000000-0000-0000-0000-000000000001", created_at=None)

@pytest.mark.asyncio
async def test_create_account(account_service, account_repository_mock, account):
    account_repository_mock.create_account.return_value = account

    result = await account_service.create_account()
    assert isinstance(result, Account)
    assert result.id == account.id

@pytest.mark.asyncio
async def test_get_account_by_id(account_service, account_repository_mock, account):
    account_repository_mock.get_account_by_id.return_value = account

    result = await account_service.get_account(UUID("00000000-0000-0000-0000-000000000001"))
    assert isinstance(result, Account)
    assert result.id == account.id

@pytest.mark.asyncio
async def test_get_account_by_id_not_found(account_service, account_repository_mock):
    account_repository_mock.get_account_by_id.return_value = None

    result = await account_service.get_account(UUID("00000000-0000-0000-0000-000000000002"))
    assert result is None