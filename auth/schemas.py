import re

from pydantic import BaseModel, field_validator

from fastapi import HTTPException


class LoginSchema(BaseModel):
    phone_number: str
    password: str

    @field_validator("phone_number")
    def check_username(cls, value):
        if not re.match(pattern=r"^\+?[1-9]\d{1,14}$", string=value):
            raise HTTPException(
                status_code=400,
                detail="Invalid phone number format",
            )
        return value
