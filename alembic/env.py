import asyncio
import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine

# ensure project root is on sys.path so `app` package imports work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database.base import Base
# import models so they are registered with Base.metadata
from app.models import role, user, category, book, borrowing, reservation  # noqa: F401
from app.core.config import settings

config = context.config
fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline():
    # Allow overriding the DB URL for Alembic operations via env var
    url = os.getenv("ALEMBIC_DATABASE_URL") or settings.database_url
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    # Allow overriding the DB URL for Alembic operations via env var
    db_url = os.getenv("ALEMBIC_DATABASE_URL") or settings.database_url
    connectable = create_async_engine(db_url)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
