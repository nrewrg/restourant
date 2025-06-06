from sqlmodel import SQLModel, Field
from sqlmodel.sql.sqltypes import AutoString

from typing import Literal

import sqlalchemy as sa

Role = Literal["user", "admin"]


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int = Field(primary_key=True)

    phone_number: str = Field(nullable=False)
    role: Role = Field(
        sa_column=sa.Column("role", AutoString(), nullable=False, default="user")
    )
    name: str | None = Field()

    hashed_password: str = Field(nullable=False)
