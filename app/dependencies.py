import os
import boto3
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.database import get_db
from app.s3client import s3_client,bucket_name
from repositories.found_pet_report_repository import FoundPetReportRepository
from repositories.image_repository import ImageRepository
from repositories.lost_pet_report_repository import LostPetReportRepository
from repositories.medical_history_repository import MedicalHistoryRepository
from repositories.pet_repository import PetRepository
from repositories.provider_phone_repository import ProviderPhoneRepository
from repositories.service_provider_location_repository import ServiceProviderLocationRepository
from repositories.service_provider_repository import ServiceProviderRepository
from repositories.sqlalchemy_found_pet_report_repository import SQLAlchemyFoundPetReportRepository
from repositories.sqlalchemy_image_repository import SQLAlchemyImageRepository
from repositories.sqlalchemy_avatar_image_repository import SQLAlchemyAvatarImageRepository
from repositories.sqlalchemy_lost_pet_report_repository import SQLAlchemyLostPetReportRepository
from repositories.sqlalchemy_medical_history_repository import SQLAlchemyMedicalHistoryRepository
from repositories.sqlalchemy_person_repository import SQLAlchemyPersonRepository
from repositories.sqlalchemy_pet_repository import SQLAlchemyPetRepository
from repositories.sqlalchemy_provider_phone_repository import SQLAlchemyProviderPhoneRepository
from repositories.sqlalchemy_service_provider_location_repository import SQLAlchemyServiceProviderLocationRepository
from repositories.sqlalchemy_service_provider_repository import SQLAlchemyServiceProviderRepository
from repositories.sqlalchemy_user_provider_repository import SQLAlchemyUserProviderRepository
from repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from repositories.sqlalchemy_working_hours_repository import SQLAlchemyWorkingHoursRepository
from repositories.user_provider_repository import UserProviderRepository
from repositories.user_repository import UserRepository
from repositories.avatar_image_repository import AvatarImageRepository
from repositories.working_hours_repository import WorkingHoursRepository
from services.email_service import EmailService
from services.email_service_implementation import EmailServiceImplementation
from services.found_pet_report_service_implementation import FoundPetReportServiceImplementation
from services.image_service_implementation import ImageServiceImplementation
from services.avatar_image_service_implementation import AvatarImageServiceImplementation
from services.lost_pet_report_service_implementation import LostPetReportServiceImplementation
from services.medical_history_service_implementation import MedicalHistoryServiceImplementation
from services.person_service_implementation import PersonServiceImplementation
from services.pet_service_implementation import PetServiceImplementation
from services.provider_phone_service_implementation import ProviderPhoneServiceImplementation
from services.service_provider_location_service_implementation import ServiceProviderLocationServiceImplementation
from services.service_provider_service_implementation import ServiceProviderServiceImplementation
from services.user_provider_service_implementation import UserProviderServiceImplementation
from services.user_service_implementation import UserServiceImplementation
from services.working_hours_service_implementation import WorkingHoursServiceImplementation



# Email Service Dependency
def get_email_service() -> EmailServiceImplementation:
    return EmailServiceImplementation()

# Person Repository and Service Dependencies
def get_person_repository() -> SQLAlchemyPersonRepository:
    return SQLAlchemyPersonRepository()

def get_person_service(repository: SQLAlchemyPersonRepository = Depends(get_person_repository)) -> PersonServiceImplementation:
    return PersonServiceImplementation(repository)

# User Repository and Service Dependencies
def get_user_repository() -> SQLAlchemyUserRepository:
    return SQLAlchemyUserRepository()

def get_user_service(
    repository: UserRepository = Depends(get_user_repository),
    email_service: EmailService = Depends(get_email_service)
) -> UserServiceImplementation:
    return UserServiceImplementation(repository, email_service)

# Image Repository and Service Dependencies
def get_image_repository() -> SQLAlchemyImageRepository:
    return SQLAlchemyImageRepository()

def get_image_service(
    repository: ImageRepository = Depends(get_image_repository),
) -> ImageServiceImplementation:
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION')
    )
    bucket_name = os.getenv('AWS_S3_BUCKET_NAME')
    return ImageServiceImplementation(repository, s3_client, bucket_name)

# Avatar Image Repository and Service Dependencies
def get_avatar_image_repository() -> SQLAlchemyAvatarImageRepository:
    return SQLAlchemyAvatarImageRepository()

def get_avatar_image_service(
    repository: AvatarImageRepository = Depends(get_avatar_image_repository),
) -> AvatarImageServiceImplementation:
    return AvatarImageServiceImplementation(repository, s3_client, bucket_name)
# Pet Repository and Service Dependencies
def get_pet_repository() -> SQLAlchemyPetRepository:
    return SQLAlchemyPetRepository()

def get_pet_service(
    repository: PetRepository = Depends(get_pet_repository)
) -> PetServiceImplementation:
    return PetServiceImplementation(repository)

# Lost Pet Report Repository and Service Dependencies
def get_lost_pet_report_repository() -> SQLAlchemyLostPetReportRepository:
    return SQLAlchemyLostPetReportRepository()

def get_lost_pet_report_service(
    repository: LostPetReportRepository = Depends(get_lost_pet_report_repository),
) -> LostPetReportServiceImplementation:
    return LostPetReportServiceImplementation(repository)

# Found Pet Report Repository and Service Dependencies
def get_found_pet_report_repository() -> SQLAlchemyFoundPetReportRepository:
    return SQLAlchemyFoundPetReportRepository()

def get_found_pet_report_service(
    repository: FoundPetReportRepository = Depends(get_found_pet_report_repository),
) -> FoundPetReportServiceImplementation:
    return FoundPetReportServiceImplementation(repository)


# Medical History Repository and Service Dependencies
def get_medical_history_repository() -> SQLAlchemyMedicalHistoryRepository:
    return SQLAlchemyMedicalHistoryRepository()

def get_medical_history_service(
    repository: MedicalHistoryRepository = Depends(get_medical_history_repository),
) -> MedicalHistoryServiceImplementation:
    return MedicalHistoryServiceImplementation(repository)


# WorkingHours Repository and Service Dependencies
def get_working_hours_repository() -> SQLAlchemyWorkingHoursRepository:
    return SQLAlchemyWorkingHoursRepository()

def get_working_hours_service(
    repository: WorkingHoursRepository = Depends(get_working_hours_repository)
) -> WorkingHoursServiceImplementation:
    return WorkingHoursServiceImplementation(repository)


# ProviderPhone Repository and Service Dependencies
def get_provider_phone_repository() -> SQLAlchemyProviderPhoneRepository:
    return SQLAlchemyProviderPhoneRepository()

def get_provider_phone_service(
    repository: ProviderPhoneRepository = Depends(get_provider_phone_repository)
) -> ProviderPhoneServiceImplementation:
    return ProviderPhoneServiceImplementation(repository)
# UserProvider Repository and Service Dependencies
def get_user_provider_repository() -> SQLAlchemyUserProviderRepository:
    return SQLAlchemyUserProviderRepository()

def get_user_provider_service(
    repository: UserProviderRepository = Depends(get_user_provider_repository)
) -> UserProviderServiceImplementation:
    return UserProviderServiceImplementation(repository)


# ServiceProvider Repository and Service Dependencies
def get_service_provider_repository() -> SQLAlchemyServiceProviderRepository:
    return SQLAlchemyServiceProviderRepository()

def get_service_provider_service(
    repository: ServiceProviderRepository = Depends(get_service_provider_repository)
) -> ServiceProviderServiceImplementation:
    return ServiceProviderServiceImplementation(repository)

# ServiceProviderLocation Repository and Service Dependencies
def get_service_provider_location_repository() -> SQLAlchemyServiceProviderLocationRepository:
    return SQLAlchemyServiceProviderLocationRepository()

def get_service_provider_location_service(
    repository: ServiceProviderLocationRepository = Depends(get_service_provider_location_repository)
) -> ServiceProviderLocationServiceImplementation:
    return ServiceProviderLocationServiceImplementation(repository)
