import uuid

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from starlette import status

from enums.role_enum import RoleEnum
from utils.jwt_helper import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        user_id: uuid.UUID = payload.user_id
        role: RoleEnum = payload.role

        return user_id, role

    except JWTError as e:
        # Differentiate based on the JWTError message
        error_message = str(e)
        if "Signature has expired" in error_message:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session has expired. Please log in again.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        elif "Invalid token" in error_message or "Invalid signature" in error_message:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token. Please log in again.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        else:
            raise credentials_exception
