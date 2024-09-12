from pydantic import BaseModel, FieldValidationInfo, field_validator, Field
import phonenumbers
from fastapi import HTTPException

class ProviderPhoneBoundary(BaseModel):
    phone_number: str = Field(..., example="+442083661177")

    # Phone number validator using phonenumbers library
    @field_validator('phone_number')
    def validate_phone_number(cls, v: str, info: FieldValidationInfo):
        try:
            phone = phonenumbers.parse(v)
            if not phonenumbers.is_valid_number(phone):
                raise HTTPException(status_code=400, detail='Invalid phone number format')
            return phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.E164)  # Return E.164 format
        except phonenumbers.NumberParseException:
            raise HTTPException(status_code=400, detail='Invalid phone number format')

    class Config:
        from_attributes = True