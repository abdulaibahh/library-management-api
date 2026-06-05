import asyncio

from app.database.session import AsyncSessionLocal
from app.database.seed import seed_initial_data


async def main() -> None:
    async with AsyncSessionLocal() as session:
        await seed_initial_data(session)


if __name__ == "__main__":
    asyncio.run(main())
