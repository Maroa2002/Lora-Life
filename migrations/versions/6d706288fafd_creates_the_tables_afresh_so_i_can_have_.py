"""Creates the tables afresh so I can have a new start

Revision ID: 6d706288fafd
Revises: ac99c05b1fd7
Create Date: 2025-02-18 17:22:13.542023

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d706288fafd'
down_revision = 'ac99c05b1fd7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('full_name', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('phone', sa.String(length=20), nullable=False),
    sa.Column('password_hash', sa.String(length=255), nullable=False),
    sa.Column('user_role', sa.Enum('farmer', 'vet', name='user_roles'), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('farmers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('farm_name', sa.String(length=255), nullable=True),
    sa.Column('farm_location', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('vets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('specialization', sa.String(length=255), nullable=False),
    sa.Column('years_experience', sa.Integer(), nullable=False),
    sa.Column('verification_document_path', sa.String(length=255), nullable=False),
    sa.Column('clinic_name', sa.String(length=255), nullable=True),
    sa.Column('service_area', sa.Text(), nullable=False),
    sa.Column('is_verifed', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('vets')
    op.drop_table('farmers')
    op.drop_table('users')
    # ### end Alembic commands ###
