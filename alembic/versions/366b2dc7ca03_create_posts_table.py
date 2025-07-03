"""create posts table

Revision ID: 366b2dc7ca03
Revises: 
Create Date: 2025-07-03 13:11:11.173280

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '366b2dc7ca03'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("posts", 
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True, nullable=False),
        sa.Column("title", sa.String, nullable=False)
        # sa.Column("content", sa.String, nullable=False),
        # sa.Column("created_at", sa.DateTime, server_default=sa.text("now()"), nullable=False),
        # sa.Column("published", sa.Boolean, nullable=False, default=True),
        # sa.Column("rating", sa.Integer, nullable=True)
        # sa.Column("owner_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    )
    pass
    


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("posts")
    pass
