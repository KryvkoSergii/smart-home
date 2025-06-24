from sqlalchemy.ext.asyncio import AsyncSession
from repository.accounts import AccountRepository
from repository.models import Account
from uuid import UUID
from logging import Logger

class AccountService:
    def __init__(self, logger: Logger, db: AsyncSession):
        self.__logger = logger
        self.repository = AccountRepository(db)

    def get_account(self, account_id: UUID) -> Account | None:
        self.__logger.debug(f"Retrieving account with ID: {account_id}")
        return self.repository.get_account_by_id(account_id)

    def create_account(self, account_id: UUID) -> Account:
        self.__logger.info(f"Creating account with ID: {account_id}")
        account_data = Account(id=account_id)
        return self.repository.create_account(account_data)

    def delete_account(self, account_id):
        self.__logger.info(f"Deleting account with ID: {account_id}")
        return self.repository.delete_account(account_id)