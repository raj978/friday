"""Upgrade all users to admin role

Revision ID: b8e4f2a1c9d5
Revises: a5c220713937
Create Date: 2025-11-14 10:10:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b8e4f2a1c9d5"
down_revision: Union[str, None] = "a5c220713937"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    """Upgrade all pending and user roles to admin."""
    # Update all users with 'pending' or 'user' role to 'admin'
    op.execute(
        """
        UPDATE "user"
        SET role = 'admin'
        WHERE role IN ('pending', 'user')
        """
    )


def downgrade():
    """
    Downgrade is not supported for this migration.
    Role changes are intentional and cannot be automatically reverted
    without knowing the original role for each user.
    """
    pass
