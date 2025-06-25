import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.repository.users import UserRepository
from app.repository.models import User, Base
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
async def user_repo(db_session: AsyncSession):
    return UserRepository(db_session)


@pytest_asyncio.fixture()
async def predefined_user(db_session: AsyncSession):
    user = User(
        id="00000000-0000-0000-0000-000000000001",
        username="user",
        email="user@gmail.com",
        hashed_password="hash",
        created_at=datetime.now(),
        account_id="00000000-0000-0000-0000-000000000000",
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.mark.asyncio
async def test_create_user(user_repo: UserRepository):
    now = datetime.now()
    user = User(
        id="00000000-0000-0000-0000-000000000001",
        username="user",
        email="user@gmail.com",
        hashed_password="hash",
        created_at=now,
        account_id="00000000-0000-0000-0000-000000000000",
    )
    created: User = await user_repo.create_user(user)

    assert created.username == "user"
    assert created.email == "user@gmail.com"
    assert created.hashed_password == "hash"
    assert created.created_at == now
    assert created.account_id == "00000000-0000-0000-0000-000000000000"


@pytest.mark.asyncio
async def test_get_user_by_username(
    user_repo: UserRepository, predefined_user: User):
    found: User = await user_repo.get_user_by_username(predefined_user.username)
    assert found.id == predefined_user.id


@pytest.mark.asyncio
async def test_get_user_by_email(
    user_repo: UserRepository, predefined_user: User):
    found: User = await user_repo.get_user_by_email(predefined_user.email)
    assert found.id == predefined_user.id