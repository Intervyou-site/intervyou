# alembic/env.py — async-ready run_migrations_online
from __future__ import with_statement
import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy import engine_from_config
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
import os
import importlib

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# Import your models' Base here so autogenerate sees them
# e.g. from myapp.models import Base
# Replace 'fastapi_app' with your module path if needed
from fastapi_app import Base  # ensure Base is importable

target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    # priority: env var ASYNC_DATABASE_URL, else alembic.ini sqlalchemy.url
    async_url = os.environ.get("ASYNC_DATABASE_URL") or config.get_main_option("sqlalchemy.url")
    if async_url and async_url.startswith("postgres://"):
        async_url = async_url.replace("postgres://", "postgresql+asyncpg://", 1)

    connectable = create_async_engine(
        async_url,
        poolclass=pool.NullPool,
        future=True,
    )

    async with connectable.connect() as connection:  # type: Connection
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def do_run_migrations(connection: Connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        render_as_batch=True,  # helps with sqlite -> alter operations, safe for Postgres
    )

    with context.begin_transaction():
        context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
