"""empty message

Revision ID: 4db31a3dbef9
Revises: 
Create Date: 2018-02-24 16:11:29.844229

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4db31a3dbef9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('student', 'dob',
               existing_type=sa.DATE(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('student', 'dob',
               existing_type=sa.DATE(),
               nullable=False)
    # ### end Alembic commands ###
