from typing import Optional

from pydantic import BaseModel, field_validator

from fastapi import HTTPException

import re


class CreateCategorySchema(BaseModel):
    title: str
    slug: str

    @field_validator("title")
    def validate_title(cls, v: str) -> str:
        if v:
            if not re.fullmatch(r"^[A-Z][a-z]*$", v):
                raise HTTPException(status_code=400, detail="Invalid title format")
            return v

    @field_validator("slug")
    def validate_slug(cls, v: str) -> str:
        if v:
            if not re.fullmatch(r"^[a-z]+$", v):
                raise HTTPException(status_code=400, detail="Invalid slug format")
            return v


class UpdateCategorySchema(CreateCategorySchema):
    title: Optional[str] = None
    slug: Optional[str] = None
