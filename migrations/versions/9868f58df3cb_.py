"""empty message

Revision ID: 9868f58df3cb
Revises: 866f24677210
Create Date: 2018-03-01 10:07:14.769667

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9868f58df3cb'
down_revision = '866f24677210'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('faculty', sa.Column('facultyId', sa.String(length=255), nullable=True))
    op.create_unique_constraint(None, 'faculty', ['facultyId'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'faculty', type_='unique')
    op.drop_column('faculty', 'facultyId')
    # ### end Alembic commands ###
