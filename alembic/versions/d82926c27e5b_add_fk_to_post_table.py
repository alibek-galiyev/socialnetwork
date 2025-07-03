"""add FK to post table

Revision ID: d82926c27e5b
Revises: 45291e158d36
Create Date: 2025-07-03 13:28:55.029327

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd82926c27e5b'
down_revision: Union[str, Sequence[str], None] = '45291e158d36'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("created_at", sa.DateTime, server_default=sa.text("now()"), nullable=False))
    op.add_column("posts", sa.Column("published", sa.Boolean, server_default="true", nullable=False))
    op.add_column("posts", sa.Column("rating", sa.Integer, nullable=True))
    op.add_column("posts", sa.Column("owner_id", sa.Integer, nullable=False))
    op.create_foreign_key(
        "fk_posts_owner_id_users_id",
        source_table = "posts",
        referent_table = "users",
        local_cols = ["owner_id"],
        remote_cols = ["id"],
        ondelete="CASCADE"
    )
    
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("fk_posts_owner_id_users_id", table_name="posts")
    op.drop_column("posts", "owner_id")
    op.drop_column("posts", "rating")
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
