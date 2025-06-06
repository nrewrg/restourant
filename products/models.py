from sqlmodel import SQLModel, Field


class Product(SQLModel, table=True):
    __tablename__ = "products"

    id: int = Field(primary_key=True)

    title: str = Field(nullable=False)
    description: str = Field(nullable=False)
    price: float = Field(nullable=False, default=0.0)

    image: str = Field(nullable=False)

    category_id: int = Field(foreign_key="categories.id", ondelete="CASCADE")
