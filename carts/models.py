from typing import Union

from sqlmodel import SQLModel, Field

import sqlalchemy as sa


class Cart(SQLModel, table=True):
    __tablename__ = "carts"

    user_id: int = Field(primary_key=True, foreign_key="users.id", unique=True)

    products: dict[str, dict[str, Union[int, float]]] = Field(
        sa_column=sa.Column("products", sa.JSON(), nullable=False, default={})
    )
    total_price: float = Field(nullable=False, default=0.0)
