from sqlmodel import SQLModel, Field

from datetime import datetime


class Reservation(SQLModel, table=True):
    __tablename__ = "reservations"

    id: int = Field(primary_key=True)

    user_id: int = Field(foreign_key="users.id", ondelete="CASCADE")

    time: datetime = Field(nullable=False)
