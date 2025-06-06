"""create orders table

Revision ID: b693b47fac72
Revises: 10f248f85845
Create Date: 2025-05-01 11:41:43.271522

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from sqlmodel.sql.sqltypes import AutoString


# revision identifiers, used by Alembic.
revision: str = "b693b47fac72"
down_revision: Union[str, None] = "10f248f85845"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "orders",
        sa.Column("id", sa.Integer()),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("products", sa.JSON(), nullable=False),
        sa.Column("total_price", sa.Float(), nullable=False),
        sa.Column("status", AutoString(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
    )


def downgrade() -> None:
    op.drop_table("orders")
