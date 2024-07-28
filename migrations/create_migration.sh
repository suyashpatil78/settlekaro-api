MIGRATIONS_DIR="."
SQL_DIR="$MIGRATIONS_DIR/sql"
VERSIONS_DIR="$MIGRATIONS_DIR/versions"

latest_major_version=$(ls "$SQL_DIR" | grep -E '^[0-9]+\.sql$' | cut -d'_' -f1 | sort -nr | head -n 1)

next_major_version=$(expr $latest_major_version + 1)

# Get the current date
export current_date=$(date '+%Y-%m-%d')

# Create the migration script content
migration_content=$(cat <<EOF
"""
Revision ID: $(printf "%03d" "$next_major_version")
Revision Description: <migration changes description>
Create Date: ${current_date}
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
EOF
)

# Create SQL file
sql_file="$SQL_DIR/$(printf "%03d" "$next_major_version").sql"
echo "SELECT NOW()" > "${sql_file}"
echo "Created SQL file: ${sql_file}"

# Create Python file
version_file="$VERSIONS_DIR/$(printf "%03d" "$next_major_version").py"
echo "${migration_content}" > "${version_file}"
echo "Created migration file: ${version_file}"