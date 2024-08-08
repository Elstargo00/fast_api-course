"""create phone number for user column

Revision ID: 5bc79bea7099
Revises: 
Create Date: 2024-08-01 18:53:39.317400

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


from sqlalchemy.sql import table, column
from sqlalchemy import Integer, String

# revision identifiers, used by Alembic.
revision: str = '5bc79bea7099'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



connection = op.get_bind()

users = table("users", column("id", Integer), column("phone_number", String))




def upgrade() -> None:
    
    op.add_column("users", sa.Column("phone_number", sa.String(), nullable=True))
    
    
    connection.execute(
        users.update()
        .where(users.c.id == '1')
        .values({users.c.phone_number: "0634445555"})
    )
    
    
    connection.execute(
        users.update()
        .where(users.c.id == '2')
        .values({users.c.phone_number: "0834445555"})
    )
    
    op.alter_column("users", "phone_number", nullable=False)

    

def downgrade() -> None:
    op.drop_column("users", "phone_number")