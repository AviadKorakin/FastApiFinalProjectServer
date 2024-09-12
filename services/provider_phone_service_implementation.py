from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from typing import List
import uuid
from entities.provider_phone_entity import ProviderPhoneEntity
from repositories.provider_phone_repository import ProviderPhoneRepository
from services.provider_phone_service import ProviderPhoneService
from boundaries.provider_phone_boundary import ProviderPhoneBoundary
from errors.database_error import DatabaseError
from errors.validation_error import ValidationError

class ProviderPhoneServiceImplementation(ProviderPhoneService):

    def __init__(self, repository: ProviderPhoneRepository):
        self.repository = repository

    async def add_phone(self, provider_id: uuid.UUID, phone_boundary: ProviderPhoneBoundary, db: AsyncSession) -> ProviderPhoneEntity:
        phone = ProviderPhoneEntity(
            phone_id=uuid.uuid4(),
            provider_id=provider_id,
            phone_number=phone_boundary.phone_number
        )
        try:
            saved_phone = await self.repository.add_phone(phone, db)
            await db.commit()
            return saved_phone
        except IntegrityError as e:
            await db.rollback()
            error_message = str(e.orig)
            if "unique constraint" in error_message:
                raise ValidationError(f"Phone number '{phone_boundary.phone_number}' already exists for provider.")
            if "foreign key constraint" in error_message:
                raise ValidationError(f"Invalid provider ID: {provider_id}.")
            raise ValidationError(f"Failed to commit phone number: {error_message}")
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseError(f"Unexpected error during phone number creation: {str(e)}")

    async def add_phones_bulk(self, provider_id: uuid.UUID, phones: List[ProviderPhoneBoundary], db: AsyncSession) -> List[ProviderPhoneEntity]:
        phone_entities = [
            ProviderPhoneEntity(
                phone_id=uuid.uuid4(),
                provider_id=provider_id,
                phone_number=phone.phone_number
            ) for phone in phones
        ]
        try:
            saved_phones = await self.repository.add_phones_bulk(phone_entities, db)
            await db.commit()
            return saved_phones
        except IntegrityError as e:
            await db.rollback()
            error_message = str(e.orig)
            if "unique constraint" in error_message:
                raise ValidationError("One or more phone numbers already exist for the provider.")
            if "foreign key constraint" in error_message:
                raise ValidationError(f"Invalid provider ID: {provider_id}.")
            raise ValidationError(f"Failed to commit phone numbers in bulk: {error_message}")
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseError(f"Unexpected error during phone numbers creation: {str(e)}")

    async def remove_phone(self, phone_id: uuid.UUID, db: AsyncSession) -> None:
        try:
            await self.repository.remove_phone(phone_id, db)
            await db.commit()
        except ValueError as e:
            await db.rollback()
            raise ValidationError(f"Phone removal failed: {str(e)}")
        except IntegrityError as e:
            await db.rollback()
            raise ValidationError(f"Failed to remove phone: {str(e)}")
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseError(f"Unexpected error during phone number removal: {str(e)}")

    async def get_phones_by_provider_id(self, provider_id: uuid.UUID, db: AsyncSession, skip: int = 0, limit: int = 10) -> List[ProviderPhoneEntity]:
        try:
            return await self.repository.get_phones_by_provider_id(provider_id, db, skip, limit)
        except SQLAlchemyError as e:
            raise DatabaseError(f"Error fetching phones by provider: {str(e)}")

    async def get_all_phones(self, db: AsyncSession, skip: int = 0, limit: int = 10) -> List[ProviderPhoneEntity]:
        try:
            return await self.repository.get_all_phones(db, skip, limit)
        except SQLAlchemyError as e:
            raise DatabaseError(f"Error fetching all phones: {str(e)}")
