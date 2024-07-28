"""
Revision ID: 001
Revision Description: <migration changes description>
Create Date: 2024-07-28
"""

import os
import inspect

from alembic import op
from sqlalchemy import text

current_file_name = inspect.getfile(inspect.currentframe())
file_name_with_extension = current_file_name.split('/')[-1]
version = file_name_with_extension.split('.py')[0]

revision = version
down_revision = None
branch_labels = None
depends_on = None

# Define the corresponding SQL file path
corresponding_sql_file = f"migrations/sql/{version}.sql"

def upgrade() -> None:
    if not os.path.exists(f"{corresponding_sql_file}"):
        raise Exception(f"{corresponding_sql_file} file does not exist")

    file_names = [f"{corresponding_sql_file}"]
    for file in file_names:
        with open(file, encoding='utf8') as fo:
            sql = fo.read()

        connection = op.get_bind()
        connection.execute(text(sql), {"alembic_version": version})
