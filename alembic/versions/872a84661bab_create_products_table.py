"""create products table

Revision ID: 872a84661bab
Revises: 34e34e877227
Create Date: 2025-04-30 06:09:01.596359

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from sqlmodel.sql.sqltypes import AutoString


# revision identifiers, used by Alembic.
revision: str = "872a84661bab"
down_revision: Union[str, None] = "34e34e877227"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "products",
        sa.Column("id", sa.Integer()),
        sa.Column("title", AutoString(), nullable=False),
        sa.Column("description", AutoString(), nullable=True),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("image", AutoString(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["category_id"], ["categories.id"], ondelete="CASCADE"),
    )


def downgrade() -> None:
    op.drop_table("products")
