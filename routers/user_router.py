from fastapi import APIRouter, HTTPException, Path, Query, Depends, Request
from app.dependencies import get_user_service
from services.user_service import UserService
from boundaries.user_boundary import UserBoundary
from boundaries.new_user_boundary import NewUserBoundary


def get_user_router() -> APIRouter:
    router = APIRouter()

    @router.post("/", response_model=UserBoundary,summary="Register")
    async def create_new_user(
            new_user: NewUserBoundary,
            request: Request,  # Inject the Request object to get the base URL
            service: UserService = Depends(get_user_service),
    ):
        try:
            # Use request.url_for to dynamically generate the verification URL
            verification_url = str(
                request.url_for('verify_user_email', email=new_user.email, token='REPLACE_WITH_TOKEN'))
            verification_url = verification_url.replace('REPLACE_WITH_TOKEN', '{token}')

            return service.create_user(
                email=new_user.email,
                password=new_user.password,
                role=new_user.role.name,
                username=new_user.username,
                avatar=new_user.avatar,
                verification_url=verification_url
            )
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.post("/login/", response_model=UserBoundary,summary="User Login")
    async def login_user(
            email: str,
            password: str,
            service: UserService = Depends(get_user_service),
    ):
        try:
            user = service.login_user(email=email, password=password)
            return UserBoundary(
                email=user.email,
                role=user.role,
                username=user.username,
                avatar=user.avatar
            )
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.get("/", response_model=list[UserBoundary])
    async def read_users(
            page: int = Query(1, ge=1),
            size: int = Query(10, ge=1),
            service: UserService = Depends(get_user_service),
    ):
        try:
            return service.get_users(page=page, size=size)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.get("/{email}/", response_model=UserBoundary)
    async def get_user_by_email(
            email: str = Path(...),
            service: UserService = Depends(get_user_service),
    ):
        user = service.get_user_by_email(email)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    @router.get("/verify-email/{email}/{token}/", name="verify_user_email")
    async def verify_user_email(
            email: str,
            token: str,
            service: UserService = Depends(get_user_service),
    ):
        if service.verify_email(email=email, token=token):
            return {"message": "Email verified successfully."}
        raise HTTPException(status_code=400, detail="Invalid or expired token.")

    return router
