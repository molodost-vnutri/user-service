"""Добавление ролей

Revision ID: 093850bbf92f
Revises: 
Create Date: 2024-08-03 08:08:08.368578

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '093850bbf92f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Вставляем данные в таблицу roles
    op.execute("INSERT INTO roles (role) VALUES ('Пользователь')")
    op.execute("INSERT INTO roles (role) VALUES ('Администратор')")
    op.execute("INSERT INTO roles (role) VALUES ('Модератор')")
    op.execute("INSERT INTO roles (role) VALUES ('Техническая поддержка')")


def downgrade() -> None:
    op.execute("DELETE FROM roles WHERE role IN ('Пользователь', 'Администратор', 'Модератор', 'Техническая поддержка')")