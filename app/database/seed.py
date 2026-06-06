from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.roles import UserRole
from app.core.security import hash_password
from app.models.role import Role
from app.models.user import User


async def seed_initial_data(session: AsyncSession) -> None:
    roles: dict[str, Role] = {}
    for role_name in (UserRole.admin.value, UserRole.librarian.value, UserRole.student.value):
        result = await session.execute(select(Role).where(Role.name == role_name))
        role = result.scalar_one_or_none()
        if role is None:
            role = Role(name=role_name)
            session.add(role)
            await session.flush()
        roles[role_name] = role

    result = await session.execute(select(User).where(User.email == "admin@library.local"))
    admin_user = result.scalar_one_or_none()
    if admin_user is not None:
        await session.commit()
        return

    admin_user = User(
        first_name="Admin",
        last_name="User",
        email="admin@library.local",
        phone="0000000000",
        password_hash=hash_password("admin123"),
        role=roles[UserRole.admin.value],
    )
    session.add(admin_user)
    await session.commit()
