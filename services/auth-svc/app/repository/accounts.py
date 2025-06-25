from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .models import Account
from uuid import UUID


class AccountRepository:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_account_by_id(self, id: UUID) -> Account | None:
        stmt = select(Account).filter_by(id=str(id))
        account = await self.db.execute(stmt)
        return account.scalar_one_or_none()

    async def create_account(self, account: Account) -> Account:
        self.db.add(account)
        await self.db.commit()
        await self.db.refresh(account)
        return account
    
    async def delete_account(self, id: UUID) -> None:
        account = await self.get_account_by_id(id)
        if account:
            await self.db.delete(account)
            await self.db.commit()
        else:
            raise ValueError(f"Account with id {id} does not exist")
