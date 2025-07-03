"""add columns

Revision ID: 3830d27a18f4
Revises: 366b2dc7ca03
Create Date: 2025-07-03 13:20:38.593427

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3830d27a18f4'
down_revision: Union[str, Sequence[str], None] = '366b2dc7ca03'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("content", sa.String, nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "content")
    pass
