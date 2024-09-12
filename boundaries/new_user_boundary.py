import re

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, Field, field_validator
from pydantic_core.core_schema import FieldValidationInfo
from zxcvbn import zxcvbn
import phonenumbers

from enums.role_enum import RoleEnum


class NewUserBoundary(BaseModel):
    email: EmailStr
    password: str
    first_name: str = Field(..., example="John")
    last_name: str = Field(..., example="Doe")
    phone_number: str = Field(..., example="+442083661177")
    role: RoleEnum

    # Validator for first_name
    @field_validator('first_name')
    def validate_first_name(cls, v: str, info: FieldValidationInfo):
        if not re.match(r'^[A-Z][a-zA-Z]*$', v):
            raise HTTPException(status_code=400, detail="First name must start with a capital letter and contain only alphabetic characters.")
        return v

    # Validator for last_name
    @field_validator('last_name')
    def validate_last_name(cls, v: str, info: FieldValidationInfo):
        if not re.match(r'^[A-Z][a-zA-Z]*$', v):
            raise HTTPException(status_code=400, detail="Last name must start with a capital letter and contain only alphabetic characters.")
        return v

    @field_validator('phone_number')
    def validate_phone_number(cls, v: str, info: FieldValidationInfo):
        try:
            phone = phonenumbers.parse(v)
            if not phonenumbers.is_valid_number(phone):
                raise HTTPException(status_code=400, detail='Invalid phone number format')
            return phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.E164)  # Return E.164 format
        except phonenumbers.NumberParseException:
            raise HTTPException(status_code=400, detail='Invalid phone number format')

    @field_validator('password')
    def validate_password(cls, v: str):
        result = zxcvbn(v)
        score = result['score']
        if score < 3:
            suggestions = result['feedback']['suggestions']
            feedback_message = "Password is too weak."
            feedback_message += " ".join(suggestions)
            raise HTTPException(status_code=400, detail=feedback_message)
        return v

    class Config:
        from_attributes = True
