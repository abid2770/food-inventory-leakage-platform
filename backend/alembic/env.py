from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import settings
from app.database.base import Base

# Import all models so Alembic can detect them
from app.models.organization import Organization
from app.models.role import Role
from app.models.permission import Permission
from app.models.role_permission import RolePermission
from app.models.user import User
from app.models.warehouse import Warehouse
from app.models.unit import Unit
from app.models.category import Category
from app.models.supplier import Supplier
from app.models.customer import Customer
from app.models.reason import Reason
from app.models.product import Product
from app.models.bom import BOM

# Alembic Config object
config = context.config

# Configure Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# SQLAlchemy metadata
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in offline mode."""

    url = settings.DATABASE_URL

    # Alembic migration generation uses SQLAlchemy's synchronous
    # migration interface. Convert asyncpg URL to psycopg-compatible
    # URL for Alembic offline mode.
    if "+asyncpg" in url:
        url = url.replace("+asyncpg", "")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in online mode."""

    database_url = settings.DATABASE_URL

    # Alembic requires a synchronous SQLAlchemy driver for its
    # migration connection.
    sync_database_url = database_url.replace(
        "postgresql+asyncpg://",
        "postgresql+psycopg://",
    )

    connectable = create_async_engine(
        database_url,
        poolclass=pool.NullPool,
    )

    async def run_async_migrations() -> None:
        async with connectable.connect() as connection:
            await connection.run_sync(
                lambda sync_connection: context.configure(
                    connection=sync_connection,
                    target_metadata=target_metadata,
                )
            )

            async with connection.begin():
                await connection.run_sync(
                    lambda sync_connection: context.run_migrations()
                )

        await connectable.dispose()

    import asyncio

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()