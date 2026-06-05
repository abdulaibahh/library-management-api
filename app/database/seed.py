from sqlalchemy.ext.asyncio import AsyncSession

from app.core.roles import UserRole
from app.core.security import hash_password
from app.models.role import Role
from app.models.user import User


async def seed_initial_data(session: AsyncSession) -> None:
    admin_role = Role(name=UserRole.admin.value)
    librarian_role = Role(name=UserRole.librarian.value)
    student_role = Role(name=UserRole.student.value)

    session.add_all([admin_role, librarian_role, student_role])
    await session.commit()

    admin_user = User(
        first_name="Admin",
        last_name="User",
        email="admin@library.local",
        phone="0000000000",
        password_hash=hash_password("admin123"),
        role=admin_role,
    )
    session.add(admin_user)
    await session.commit()
