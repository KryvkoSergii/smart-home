import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.repository.accounts import AccountRepository
from app.repository.models import Account, Base
from datetime import datetime
import pytest_asyncio

DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine = create_async_engine(DATABASE_URL, echo=True)
TestingSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

@pytest_asyncio.fixture()
async def db_session():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    async with TestingSessionLocal() as session:
        yield session


@pytest_asyncio.fixture()
async def account_repo(db_session: AsyncSession):
    return AccountRepository(db_session)


@pytest_asyncio.fixture()
async def predefined_account(db_session: AsyncSession):
    account = Account(id="00000000-0000-0000-0000-000000000001")
    db_session.add(account)
    await db_session.commit()
    await db_session.refresh(account)
    return account

@pytest.mark.asyncio
async def test_create_account(account_repo: AccountRepository):
    now = datetime.now()
    account = Account(
        id="00000000-0000-0000-0000-000000000001",
        created_at=now,
    )
    created: Account = await account_repo.create_account(account)

    assert created.created_at == now
    assert created.id == account.id


@pytest.mark.asyncio
async def test_get_account_by_id(
    account_repo: AccountRepository, predefined_account: Account):
    found: Account = await account_repo.get_account_by_id(predefined_account.id)
    assert found.id == predefined_account.id