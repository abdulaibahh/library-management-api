import asyncio
from collections.abc import Generator

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.core.roles import UserRole
from app.database.base import Base
from app.database.seed import seed_initial_data
from app.models.book import Book
from app.models.borrowing import Borrowing
from app.models.category import Category
from app.models.reservation import Reservation
from app.models.role import Role
from app.models.user import User


@pytest.fixture()
def sessionmaker() -> Generator[async_sessionmaker[AsyncSession], None, None]:
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    testing_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async def setup_database() -> None:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    asyncio.run(setup_database())
    yield testing_session
    asyncio.run(engine.dispose())


def test_seed_initial_data_is_idempotent(sessionmaker: async_sessionmaker[AsyncSession]) -> None:
    async def run_seed_twice() -> tuple[list[str], int]:
        async with sessionmaker() as session:
            await seed_initial_data(session)
            await seed_initial_data(session)

            roles_result = await session.execute(select(Role.name).order_by(Role.name))
            admin_result = await session.execute(select(User).where(User.email == "admin@library.local"))
            return list(roles_result.scalars()), len(admin_result.scalars().all())

    role_names, admin_count = asyncio.run(run_seed_twice())

    assert role_names == sorted(role.value for role in UserRole)
    assert admin_count == 1
