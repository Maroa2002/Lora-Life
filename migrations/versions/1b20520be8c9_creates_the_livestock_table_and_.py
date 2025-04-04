"""creates the livestock table and livestock health data table and defines the relationships it has with other tables

Revision ID: 1b20520be8c9
Revises: 15e9bb5db020
Create Date: 2025-03-14 16:55:48.067315

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1b20520be8c9'
down_revision = '15e9bb5db020'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('livestock',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('farmer_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('breed', sa.String(length=255), nullable=False),
    sa.Column('weight', sa.Float(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['farmer_id'], ['farmers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('livestock_health',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('livestock_id', sa.Integer(), nullable=False),
    sa.Column('temperature', sa.Float(), nullable=False),
    sa.Column('pulse', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['livestock_id'], ['livestock.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('appointments', schema=None) as batch_op:
        batch_op.add_column(sa.Column('livestock_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'livestock', ['livestock_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('appointments', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('livestock_id')

    op.drop_table('livestock_health')
    op.drop_table('livestock')
    # ### end Alembic commands ###
