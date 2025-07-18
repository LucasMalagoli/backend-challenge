"""initial seed

Revision ID: b4983391eb34
Revises: 03e0d43d9166
Create Date: 2025-07-18 09:44:13.393046

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b4983391eb34'
down_revision: Union[str, Sequence[str], None] = '03e0d43d9166'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute(
        """
        INSERT INTO role (description) VALUES
        ('Administrator'),
        ('Regular User');
        """
    )

    op.execute(
        """
        INSERT INTO claim (description, active) VALUES
        ('Can read data', TRUE),
        ('Can write data', TRUE),
        ('Can delete data', TRUE);
        """
    )

    op.execute(
        """
        INSERT INTO users (name, email, password, role_id, created_at) VALUES
        ('admin', 'admin@example.com', 'GRzZ5nO0odsE',
         (SELECT id FROM role WHERE description = 'Administrator'),
         CURRENT_DATE),
        ('Fulano Ciclano', 'fulano@example.com', 'XhmWU5cTn4C7',
         (SELECT id FROM role WHERE description = 'Regular User'),
         CURRENT_DATE);
        """
    )

    op.execute(
        """
        INSERT INTO user_claim (user_id, claim_id)
        SELECT u.id, c.id
        FROM users u, claim c
        WHERE u.email = 'admin@example.com';
        """
    )

    op.execute(
        """
        INSERT INTO user_claim (user_id, claim_id)
        SELECT u.id, c.id
        FROM users u, claim c
        WHERE u.email = 'fulano@example.com' AND c.description = 'Can read data';
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DELETE FROM user_claim;")
    op.execute("DELETE FROM users WHERE email IN ('admin@example.com', 'fulano@example.com');")
    op.execute("DELETE FROM claim WHERE description IN ('Can read data', 'Can write data', 'Can delete data');")
    op.execute("DELETE FROM role WHERE description IN ('Administrator', 'Regular User');")
