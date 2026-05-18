from pydantic import BaseModel, EmailStr, Field, field_validator
import re


class Address(BaseModel):
    city: str = Field(..., min_length=2)
    pincode: str

    @field_validator("pincode")
    @classmethod
    def validate_pincode(cls, value: str):
        digits = re.sub(r"\D", "", value)

        if len(digits) != 6:
            raise ValueError("Pincode must contain exactly 6 digits")

        return digits


class ContactCard(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    phone: str
    address: Address

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str):
        digits = re.sub(r"\D", "", value)

        if len(digits) != 10:
            raise ValueError("Phone number must contain exactly 10 digits")

        return digits