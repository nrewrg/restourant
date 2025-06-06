"""create categories table

Revision ID: 34e34e877227
Revises: 7e2c052b3b6b
Create Date: 2025-04-30 04:42:10.378954

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from sqlmodel.sql.sqltypes import AutoString


# revision identifiers, used by Alembic.
revision: str = "34e34e877227"
down_revision: Union[str, None] = "7e2c052b3b6b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "categories",
        sa.Column("id", sa.Integer()),
        sa.Column("title", AutoString(), nullable=False),
        sa.Column("slug", AutoString(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slug"),
    )


def downgrade() -> None:
    op.drop_table("categories")
