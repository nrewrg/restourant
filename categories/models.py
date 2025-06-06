from sqlmodel import SQLModel, Field


class Category(SQLModel, table=True):
    __tablename__ = "categories"

    id: int = Field(primary_key=True)

    title: str = Field(nullable=False)
    slug: str = Field(nullable=False)
