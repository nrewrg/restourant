"""create users table

Revision ID: 7e2c052b3b6b
Revises:
Create Date: 2025-04-30 04:41:38.718935

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from sqlmodel.sql.sqltypes import AutoString


# revision identifiers, used by Alembic.
revision: str = "7e2c052b3b6b"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer()),
        sa.Column("phone_number", AutoString(), nullable=False),
        sa.Column("name", AutoString()),
        sa.Column("role", AutoString(), nullable=False),
        sa.Column("hashed_password", AutoString(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("phone_number"),
    )


def downgrade() -> None:
    op.drop_table("users")
