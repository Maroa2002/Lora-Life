"""Adds the table vet_availability and appointment

Revision ID: ed40609b71ca
Revises: 6d706288fafd
Create Date: 2025-02-19 12:38:19.791007

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ed40609b71ca'
down_revision = '6d706288fafd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('vet_availability',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('vet_id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.Column('end_time', sa.DateTime(), nullable=False),
    sa.Column('is_booked', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['vet_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('appointments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('farmer_id', sa.Integer(), nullable=False),
    sa.Column('vet_id', sa.Integer(), nullable=False),
    sa.Column('slot_id', sa.Integer(), nullable=False),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('status', sa.Enum('pending', 'confirmed', 'completed', 'cancelled'), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['farmer_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['slot_id'], ['vet_availability.id'], ),
    sa.ForeignKeyConstraint(['vet_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('vets', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_verified', sa.Boolean(), nullable=True))
        batch_op.drop_column('is_verifed')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vets', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_verifed', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
        batch_op.drop_column('is_verified')

    op.drop_table('appointments')
    op.drop_table('vet_availability')
    # ### end Alembic commands ###
