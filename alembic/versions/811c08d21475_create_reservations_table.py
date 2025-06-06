"""create reservations table

Revision ID: 811c08d21475
Revises: b693b47fac72
Create Date: 2025-05-02 01:26:02.414146

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "811c08d21475"
down_revision: Union[str, None] = "b693b47fac72"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "reservations",
        sa.Column("id", sa.Integer()),
        sa.Column("user_id", sa.Integer()),
        sa.Column("time", sa.DateTime()),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
    )


def downgrade() -> None:
    op.drop_table("reservations")
