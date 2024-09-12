import os
import uuid

from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Union
from pydantic import BaseModel

from enums.role_enum import RoleEnum

# Load environment variables
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))  # Token expiration time as int

class TokenData(BaseModel):
    user_id: uuid.UUID
    role: RoleEnum


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # Ensure the role is stored as its value in the token
    if 'role' in to_encode and isinstance(to_encode['role'], RoleEnum):
        to_encode['role'] = to_encode['role'].value  # Convert Enum to its string value

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        role: str = payload.get("role")

        if user_id is None or role is None:
            raise JWTError("Missing user_id or role in token")

        # Convert role back to RoleEnum
        role_enum = RoleEnum(role)
        user_id_uuid = uuid.UUID(user_id)  # Ensure user_id is a valid UUID

        return TokenData(user_id=user_id_uuid, role=role_enum)

    except JWTError as e:
        # Catch any JWT-related error, including expired tokens
        raise JWTError(str(e))  # Just propagate the error for now