"""new test database

Revision ID: 858fe260e8c6
Revises: 
Create Date: 2025-03-10 20:24:50.942558

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '858fe260e8c6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=255), nullable=False),
    sa.Column('last_name', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('phone', sa.String(length=20), nullable=False),
    sa.Column('password_hash', sa.String(length=255), nullable=False),
    sa.Column('user_role', sa.String(length=20), nullable=False),
    sa.Column('profile_picture', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('admins',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('role', sa.Enum('super', 'moderator', name='admin_roles'), nullable=False),
    sa.Column('permissions', sa.JSON(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('farmers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('farm_name', sa.String(length=255), nullable=True),
    sa.Column('livestock_type', sa.String(length=255), nullable=False),
    sa.Column('animal_count', sa.Integer(), nullable=False),
    sa.Column('alert_preference', sa.Enum('email', 'sms', 'whatsapp', 'app', name='alert_preferences'), nullable=False),
    sa.Column('preferred_language', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('locations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('county', sa.String(length=255), nullable=False),
    sa.Column('town', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('vet_availability',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('vet_id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.Column('end_time', sa.DateTime(), nullable=False),
    sa.Column('is_booked', sa.Boolean(), nullable=False),
    sa.Column('available_days', sa.JSON(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['vet_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('license_number', sa.String(length=255), nullable=False),
    sa.Column('experience_years', sa.Integer(), nullable=False),
    sa.Column('specialization', sa.String(length=255), nullable=False),
    sa.Column('verification_document_path', sa.String(length=255), nullable=False),
    sa.Column('clinic_name', sa.String(length=255), nullable=True),
    sa.Column('avg_rating', sa.Float(), nullable=True),
    sa.Column('is_verified', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('license_number'),
    sa.UniqueConstraint('user_id')
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
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('appointments')
    op.drop_table('vets')
    op.drop_table('vet_availability')
    op.drop_table('locations')
    op.drop_table('farmers')
    op.drop_table('admins')
    op.drop_table('users')
    # ### end Alembic commands ###
