"""empty message

Revision ID: a9d4b3003779
Revises: 2169316d1ccc
Create Date: 2022-06-08 15:06:52.347682

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a9d4b3003779'
down_revision = '2169316d1ccc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('upload_file',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.String(length=30), nullable=False),
    sa.Column('fpath', sa.String(length=100), nullable=False),
    sa.Column('user_upload', sa.Boolean(), nullable=True),
    sa.Column('upload_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('upload_file')
    # ### end Alembic commands ###
