"""Change db type float to decimal(numeric)

Revision ID: 50d2e0004460
Revises: 56f861d2b4a4
Create Date: 2025-04-21 15:09:18.349797

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '50d2e0004460'
down_revision: Union[str, None] = '56f861d2b4a4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('transactions', 'source_amount',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               type_=sa.Numeric(),
               existing_nullable=False)
    op.alter_column('transactions', 'conversion_rate',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               type_=sa.Numeric(),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('transactions', 'conversion_rate',
               existing_type=sa.Numeric(),
               type_=sa.DOUBLE_PRECISION(precision=53),
               existing_nullable=False)
    op.alter_column('transactions', 'source_amount',
               existing_type=sa.Numeric(),
               type_=sa.DOUBLE_PRECISION(precision=53),
               existing_nullable=False)
    # ### end Alembic commands ###
