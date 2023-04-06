"""add ingredients to table

Revision ID: ef07a21ad4c4
Revises: 639dba18421c
Create Date: 2023-04-06 19:24:56.446824

"""
from app.config import settings
import asyncpg
from sqlalchemy.util import await_only
# revision identifiers, used by Alembic.
from alembic import op

revision = 'ef07a21ad4c4'
down_revision = '639dba18421c'
branch_labels = None
depends_on = None

async def insert_ingredients():
    pool = await asyncpg.create_pool(
            user=settings.DB_USER,
            password=settings.DB_PASS,
            database=settings.DB_NAME,
            host=settings.DB_HOST
        )
    async with pool.acquire() as conn:
        conn.execute(
            "INSERT INTO ingredients (name, measurement_unit) "
            "VALUES ('Помидор', 'шт')")
    # ### end Alembic commands ###
    await pool.close()



def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        "INSERT INTO ingredients (name, measurement_unit) VALUES "
        "('Помидор', 'шт'), "
        "('Огурец', 'шт'), "
        "('Майонез', 'столовая ложка'),"
        "('Болгарский перец', 'шт'),"
        "('Картофель', 'шт'),"
        "('Лук', 'шт'),"
        "('Зеленый лук', 'перо'),"
        "('Свекла', 'шт')"
    )


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
