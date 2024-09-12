from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.future import select
from typing import List
from entities.provider_phone_entity import ProviderPhoneEntity
from repositories.provider_phone_repository import ProviderPhoneRepository
import uuid

class SQLAlchemyProviderPhoneRepository(ProviderPhoneRepository):

    async def add_phone(self, phone: ProviderPhoneEntity, db: AsyncSession) -> ProviderPhoneEntity:
        db.add(phone)
        await db.flush()  # Await the flush operation
        await db.refresh(phone)  # Await the refresh to get the latest data
        return phone

    async def add_phones_bulk(self, phones: List[ProviderPhoneEntity], db: AsyncSession) -> List[ProviderPhoneEntity]:
        db.add_all(phones)
        await db.flush()  # Await the flush operation
        return phones

    async def remove_phone(self, phone_id: uuid.UUID, db: AsyncSession) -> None:
        phone = await db.get(ProviderPhoneEntity, phone_id)
        if phone:
            await db.delete(phone)
            await db.flush()  # Await flush to execute deletion
        else:
            raise ValueError(f"Phone with ID {phone_id} not found.")

    async def get_phones_by_provider_id(self, provider_id: uuid.UUID, db: AsyncSession, skip: int = 0, limit: int = 10) -> List[ProviderPhoneEntity]:
        stmt = select(ProviderPhoneEntity).where(ProviderPhoneEntity.provider_id == provider_id)\
                                          .order_by(ProviderPhoneEntity.phone_number)\
                                          .offset(skip)\
                                          .limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()

    async def get_all_phones(self, db: AsyncSession, skip: int = 0, limit: int = 10) -> List[ProviderPhoneEntity]:
        stmt = select(ProviderPhoneEntity).order_by(ProviderPhoneEntity.provider_id, ProviderPhoneEntity.phone_number)\
                                          .offset(skip)\
                                          .limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()
