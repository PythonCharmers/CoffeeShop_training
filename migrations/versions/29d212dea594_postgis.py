"""Set up the database to include PostGIS

Revision ID: 29d212dea594
Revises: 
Create Date: 2019-01-24 10:07:52.688033

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '29d212dea594'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute('create extension if not exists postgis')


def downgrade():
    op.execute('drop extension postgis')
