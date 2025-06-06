from pydantic import BaseModel, field_validator

from fastapi import HTTPException

import re


class CreateUserSchema(BaseModel):
    phone_number: str
    name: str | None = None

    password: str

    @field_validator("phone_number")
    def validate_phone_number(cls, v: str) -> str:
        if v:
            if not re.fullmatch(r"^\+[1-9]\d{1,14}$", v):
                raise HTTPException(
                    status_code=400, detail="Invalid phone number format"
                )
            return v

    @field_validator("name")
    def validate_name(cls, v: str) -> str:
        if v:
            if not re.fullmatch(r"^[A-Za-z]+( [A-Za-z]+)*$", v):
                raise HTTPException(status_code=400, detail="Invalid name format")
            return v


class UpdateUserSchema(CreateUserSchema):
    phone_number: str | None = None
    password: str | None = None


class CreateAdminSchema(CreateUserSchema):
    secret: str
