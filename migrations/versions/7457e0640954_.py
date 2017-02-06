"""empty message

Revision ID: 7457e0640954
Revises: 
Create Date: 2017-02-06 16:14:37.804992

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7457e0640954'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=True),
    sa.Column('TIN', sa.String(length=11), nullable=True),
    sa.Column('phone_number', sa.String(length=10), nullable=True),
    sa.Column('address', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('TIN'),
    sa.UniqueConstraint('name')
    )
    op.create_table('items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=True),
    sa.Column('brand', sa.String(length=50), nullable=True),
    sa.Column('tax_type', sa.Integer(), nullable=True),
    sa.Column('price', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=60), nullable=True),
    sa.Column('first_name', sa.String(length=60), nullable=True),
    sa.Column('last_name', sa.String(length=60), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('bills',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('bil_number', sa.Integer(), nullable=True),
    sa.Column('customer_id', sa.Integer(), nullable=True),
    sa.Column('customer_name', sa.String(length=60), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('brand', sa.String(length=50), nullable=True),
    sa.Column('bill_amount_1', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('bill_amount_2', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('tax_amount_1', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('tax_amount_2', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('total_bill', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bill_details',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('bill_id', sa.Integer(), nullable=True),
    sa.Column('item_id', sa.Integer(), nullable=True),
    sa.Column('item_price', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('total_price', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.ForeignKeyConstraint(['bill_id'], ['bills.id'], ),
    sa.ForeignKeyConstraint(['item_id'], ['items.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bill_details')
    op.drop_table('bills')
    op.drop_table('users')
    op.drop_table('items')
    op.drop_table('customers')
    # ### end Alembic commands ###