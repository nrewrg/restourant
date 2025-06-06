from typing import Literal, Union

from sqlmodel import SQLModel, Field
from sqlmodel.sql.sqltypes import AutoString

import sqlalchemy as sa

Status = Literal["in progress", "completed", "canceled"]


class Order(SQLModel, table=True):
    __tablename__ = "orders"

    id: int = Field(primary_key=True)

    user_id: int = Field(foreign_key="users.id")

    products: dict[str, dict[str, Union[int, float]]] = Field(
        sa_column=sa.Column("products", sa.JSON(), nullable=False, default={})
    )
    total_price: float = Field(nullable=False, default=0.0)
    status: Status = Field(
        sa_column=sa.Column(
            "status", AutoString(), nullable=False, default="in progress"
        )
    )
