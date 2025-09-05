# api/app/db.py
import os
import psycopg
from pgvector.psycopg import register_vector
from pathlib import Path

# Database connection string, fallback to Docker default
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://nicu:nicu@db:5432/nicu"
)

def ensure_schema():
    """Ensure pgvector extension exists and apply schema.sql if present."""
    with psycopg.connect(DATABASE_URL, autocommit=True) as con:
        with con.cursor() as cur:
            # Make sure pgvector extension is available
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")

            # Apply schema.sql if it exists
            schema_path = Path(__file__).with_name("schema.sql")
            if schema_path.exists():
                with open(schema_path, "r", encoding="utf-8") as f:
                    cur.execute(f.read())

def get_conn(register: bool = True):
    """Get a database connection, optionally registering pgvector."""
    con = psycopg.connect(DATABASE_URL, autocommit=True)
    if register:
        try:
            register_vector(con)
        except psycopg.ProgrammingError:
            # If extension isn't ready yet
            pass
    return con