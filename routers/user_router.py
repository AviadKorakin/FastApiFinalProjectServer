from fastapi import APIRouter, HTTPException, Path, Query, Depends, Request, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.database import get_db
from app.dependencies import get_user_service
from app.oauth2 import get_current_user, oauth2_scheme
from boundaries.update_user_boundary import UpdateUserBoundary
from enums.role_enum import RoleEnum
from services.user_service import UserService
from boundaries.user_boundary import UserBoundary
from boundaries.new_user_boundary import NewUserBoundary
from errors.not_found_error import NotFoundError
from errors.validation_error import ValidationError
from errors.database_error import DatabaseError
from utils.jwt_helper import create_access_token
from pydantic import BaseModel
import uuid


def get_user_router() -> APIRouter:
    router = APIRouter()

    @router.post("/", response_model=UserBoundary, summary="Register")
    async def create_new_user(
            new_user: NewUserBoundary,
            request: Request,
            background_tasks: BackgroundTasks,
            service: UserService = Depends(get_user_service),
            db: AsyncSession = Depends(get_db)
    ):
        try:
            # Step 1: Create the user first and get the token
            user, token = await service.create_user(
                email=new_user.email,
                password=new_user.password,
                first_name=new_user.first_name,
                last_name=new_user.last_name,
                role=new_user.role.name,
                phone_number=new_user.phone_number,
                db=db
            )

            # Step 2: Generate the verification URL with the actual token
            verification_url = str(
                request.url_for('verify_user_email', user_id=user.user_id, token=token)
            )

            # Step 3: Add the email task to the background task
            background_tasks.add_task(service.send_verification_email, user.email, verification_url)

            return user
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.post("/login/", response_model=dict, summary="User Login")
    async def login_user(
        form_data: OAuth2PasswordRequestForm = Depends(),
        service: UserService = Depends(get_user_service),
        db: AsyncSession = Depends(get_db)
    ):
        try:
            user = await service.login_user(email=form_data.username, password=form_data.password, db=db)
            # Generate the JWT token, storing the user_id (UUID) and role
            access_token = create_access_token(data={"sub": str(user.user_id), "role": user.role})

            return {"access_token": access_token, "token_type": "bearer"}
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except NotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))

    @router.get("/", response_model=list[UserBoundary], summary="List Users")
    async def read_users(
        page: int = Query(1, ge=1),
        size: int = Query(10, ge=1),
        service: UserService = Depends(get_user_service),
        db: AsyncSession = Depends(get_db),
        token: str = Depends(oauth2_scheme)
    ):
        user_id,role = get_current_user(token)  # Check for the admin role
        if role < RoleEnum.ADMIN:  # Compare roles based on rank
            raise HTTPException(status_code=403, detail="Access forbidden: higher roles only")
        try:
            return await service.get_users(page=page, size=size, db=db)
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/{user_id}/", response_model=UserBoundary, summary="Get User by ID")
    async def get_user_by_id(
        user_id:  uuid.UUID,
        service: UserService = Depends(get_user_service),
        db: AsyncSession = Depends(get_db),
        token: str = Depends(oauth2_scheme)
    ):
        try:
            user = await service.get_user_by_id(user_id=user_id, db=db)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return user
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    @router.get("/verify-email/{user_id}/{token}/", name="verify_user_email", summary="Verify User Email")
    async def verify_user_email(
        user_id: uuid.UUID,
        token: str,
        service: UserService = Depends(get_user_service),
        db: AsyncSession = Depends(get_db)
    ):
        try:
            if await service.verify_email(user_id=user_id, token=token, db=db):
                return {"message": "Email verified successfully."}
            raise HTTPException(status_code=400, detail="Invalid or expired token.")
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    @router.post("/reset-token/", summary="Reset User Token")
    async def reset_token(
            email: str,
            request: Request,
            background_tasks: BackgroundTasks,
            service: UserService = Depends(get_user_service),
            db: AsyncSession = Depends(get_db)
    ):
        try:
            # Step 1: Call the service to reset the token and get the user_id and token
            user_id, token = await service.reset_token(email=email, db=db)

            # Step 2: Generate the verification URL
            verification_url = str(
                request.url_for('verify_user_email', user_id=user_id, token=token)
            )

            # Step 3: Add the email task to background tasks
            background_tasks.add_task(service.send_verification_email, email, verification_url)

            return {"message": "Token reset email sent successfully."}

        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))  # Handle already verified
        except NotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))  # Handle user not found
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    @router.put("/update-details/{user_id}", response_model=UserBoundary, summary="Update User Details")
    async def update_user_details(
            user_id: uuid.UUID,
            user_data: UpdateUserBoundary,
            service: UserService = Depends(get_user_service),
            db: AsyncSession = Depends(get_db),
            token: str = Depends(oauth2_scheme)
    ):
        try:
            return await service.update_user_details(
                user_id=user_id,
                old_password=user_data.old_password,
                new_password=user_data.new_password,
                first_name=user_data.first_name,
                last_name=user_data.last_name,
                phone_number=user_data.phone_number,
                db=db
            )
        except NotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    return router