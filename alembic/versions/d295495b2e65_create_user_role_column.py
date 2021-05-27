"""create user role column

Revision ID: d295495b2e65
Revises: 
Create Date: 2021-05-07 23:33:38.489804

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM
from app.models.user import UserRoleEnum
from ..utils.alembic_helpers import table_has_column


# revision identifiers, used by Alembic.
revision = 'd295495b2e65'
down_revision = None
branch_labels = None
depends_on = None

table_name = 'users'
column_name = 'role'


def upgrade():
    role_enum = ENUM(UserRoleEnum,
                     values_callable=lambda enm: [e.value for e in enm],
                     name="user_role_enum")
    column_props = sa.Column(
        column_name,
        role_enum,
        nullable=False,
        default=UserRoleEnum.user.value,
        server_default=UserRoleEnum.user.value)
    if not table_has_column(table_name, column_name):
        role_enum.create(op.get_bind())
        op.add_column(table_name, column_props)


def downgrade():
    op.drop_column(table_name, column_name)
    op.execute("DROP TYPE user_role_enum;")
