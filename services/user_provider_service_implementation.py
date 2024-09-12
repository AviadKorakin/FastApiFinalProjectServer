from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from entities.user_provider_association_entity import UserProviderAssociationEntity
from repositories.user_provider_repository import UserProviderRepository
from services.user_provider_service import UserProviderService
from boundaries.user_provider_boundary import UserProviderBoundary
from errors.validation_error import ValidationError
from errors.database_error import DatabaseError
from typing import List, Optional
import uuid

class UserProviderServiceImplementation(UserProviderService):

    def __init__(self, repository: UserProviderRepository):
        self.repository = repository

    async def add_user_provider(self, boundary: UserProviderBoundary, provider_id: uuid.UUID, db: AsyncSession) -> UserProviderAssociationEntity:
        association = UserProviderAssociationEntity(
            user_email=boundary.user_email,
            provider_id=provider_id,
            role=boundary.role
        )
        try:
            association = await self.repository.add_user_provider(association, db)
            await db.commit()
            return association
        except IntegrityError as e:
            await db.rollback()
            error_message = str(e.orig)
            if "foreign key constraint" in error_message:
                raise ValidationError("Invalid user or provider ID.")
            if "unique constraint" in error_message:
                raise ValidationError(f"A user-provider association for user '{boundary.user_email}' already exists.")
            raise ValidationError(f"Failed to add user-provider association: {error_message}")
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseError(f"Unexpected error occurred while adding user-provider association: {str(e)}")

    async def add_user_providers_bulk(self, users: List[UserProviderBoundary], provider_id: uuid.UUID, db: AsyncSession) -> List[UserProviderAssociationEntity]:
        associations = [
            UserProviderAssociationEntity(
                user_email=user.user_email,
                provider_id=provider_id,
                role=user.role
            ) for user in users
        ]
        try:
            associations = await self.repository.add_user_providers_bulk(associations, db)
            await db.commit()
            return associations
        except IntegrityError as e:
            await db.rollback()
            error_message = str(e.orig)
            if "foreign key constraint" in error_message:
                raise ValidationError("One or more invalid user or provider IDs.")
            if "unique constraint" in error_message:
                raise ValidationError("One or more user-provider associations already exist.")
            raise ValidationError(f"Failed to add user-provider associations in bulk: {error_message}")
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseError(f"Unexpected error occurred while adding user-provider associations in bulk: {str(e)}")

    async def remove_user_provider(self, user_id: uuid.UUID, provider_id: uuid.UUID, db: AsyncSession) -> None:
        try:
            await self.repository.remove_user_provider(user_id, provider_id, db)
            await db.commit()
        except ValidationError as e:
            await db.rollback()
            raise ValidationError(f"Failed to remove user-provider association: {str(e)}")
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseError(f"Unexpected error occurred while removing user-provider association: {str(e)}")

    async def get_user_providers(self, user_id: Optional[uuid.UUID], provider_id: Optional[uuid.UUID], role: Optional[str],
                                 db: AsyncSession, skip: int = 0, limit: int = 10) -> List[UserProviderAssociationEntity]:
        try:
            return await self.repository.get_by_filters(user_id, provider_id, role, db, skip, limit)
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to retrieve user-provider associations: {str(e)}")
