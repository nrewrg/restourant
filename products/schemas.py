from typing import Optional

from pydantic import BaseModel, field_validator

from fastapi import HTTPException

import re


class CreateProductSchema(BaseModel):
    title: str
    description: str

    price: float

    image: str

    category_id: int

    @field_validator("image")
    def validate_phone_number(cls, v: str) -> str:
        pattern = re.compile(
            r'https?://[^\s"\'<>]+?\.(jpe?g|png|avif|webp)(\?[^"\s]*)?$', re.IGNORECASE
        )
        if v:
            if not pattern.fullmatch(v):
                raise HTTPException(status_code=400, detail="Invalid image URL format")
            return v


class UpdateProductSchema(CreateProductSchema):
    title: Optional[str] = None
    description: Optional[str] = None

    price: Optional[float] = None

    image: Optional[str] = None

    category_id: Optional[int] = None
