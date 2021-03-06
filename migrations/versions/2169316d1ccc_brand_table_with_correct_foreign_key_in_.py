"""brand table with correct foreign key in products

Revision ID: 2169316d1ccc
Revises: 495d01ee4cd2
Create Date: 2022-06-06 20:21:44.765979

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2169316d1ccc'
down_revision = '495d01ee4cd2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('brand',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=50), nullable=False),
    sa.Column('clearance', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('password')
    )
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('qty', sa.Integer(), nullable=False),
    sa.Column('brand_name', sa.String(length=20), nullable=True),
    sa.ForeignKeyConstraint(['brand_name'], ['brand.name'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('products')
    op.drop_table('user')
    op.drop_table('brand')
    # ### end Alembic commands ###
