import re
import phonenumbers
from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator
from zxcvbn import zxcvbn
from typing import Optional

class UpdateUserBoundary(BaseModel):
    old_password: str
    new_password: Optional[str] = None
    first_name: Optional[str] = Field(None, example="John")
    last_name: Optional[str] = Field(None, example="Doe")
    phone_number: Optional[str] = Field(None, example="+442083661177")

    # Validator for first_name
    @field_validator('first_name')
    def validate_first_name(cls, v: Optional[str]):
        if v and not re.match(r'^[A-Z][a-zA-Z]*$', v):
            raise HTTPException(status_code=400, detail="First name must start with a capital letter and contain only alphabetic characters.")
        return v

    # Validator for last_name
    @field_validator('last_name')
    def validate_last_name(cls, v: Optional[str]):
        if v and not re.match(r'^[A-Z][a-zA-Z]*$', v):
            raise HTTPException(status_code=400, detail="Last name must start with a capital letter and contain only alphabetic characters.")
        return v

    @field_validator('phone_number')
    def validate_phone_number(cls, v: Optional[str]):
        if v:
            try:
                phone = phonenumbers.parse(v)
                if not phonenumbers.is_valid_number(phone):
                    raise HTTPException(status_code=400, detail='Invalid phone number format')
                return phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.E164)
            except phonenumbers.NumberParseException:
                raise HTTPException(status_code=400, detail='Invalid phone number format')
        return v

    @field_validator('new_password')
    def validate_password(cls, v: Optional[str]):
        if v:
            result = zxcvbn(v)
            score = result['score']
            if score < 3:
                suggestions = result['feedback']['suggestions']
                feedback_message = "Password is too weak. "
                feedback_message += " ".join(suggestions)
                raise HTTPException(status_code=400, detail=feedback_message)
        return v

    class Config:
        from_attributes = True
