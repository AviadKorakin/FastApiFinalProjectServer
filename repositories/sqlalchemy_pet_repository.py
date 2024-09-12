import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from entities.pet_entity import PetEntity
from repositories.pet_repository import PetRepository
from typing import List, Type
from sqlalchemy import select


class SQLAlchemyPetRepository(PetRepository):

    async def create(self, pet: PetEntity, db: AsyncSession) -> PetEntity:
        db.add(pet)
        await db.flush()
        await db.refresh(pet)
        return pet

    async def update(self, pet: PetEntity, db: AsyncSession) -> PetEntity:
        await db.flush()
        await db.refresh(pet)
        return pet

    async def get_by_pet_id(self, pet_id: uuid.UUID, db: AsyncSession) -> PetEntity | None:
        result = await db.execute(
            select(PetEntity).filter_by(pet_id=pet_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self, skip: int, limit: int, db: AsyncSession) -> List[PetEntity]:
        result = await db.execute(
            select(PetEntity).order_by(PetEntity.name).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def get_by_user_id(self, user_id: uuid.UUID, skip: int, limit: int, db: AsyncSession) -> List[PetEntity]:
        result = await db.execute(
            select(PetEntity).where(PetEntity.user_id == user_id).order_by(PetEntity.name).offset(skip).limit(limit)
        )
        return result.scalars().all()
