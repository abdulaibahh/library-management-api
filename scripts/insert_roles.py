import asyncio
import asyncpg

async def main():
    conn = await asyncpg.connect('postgresql://postgres:Wayancity087@localhost:5432/library_management_db')
    await conn.execute("INSERT INTO roles (name) VALUES ('student'), ('librarian'), ('admin') ON CONFLICT DO NOTHING;")
    rows = await conn.fetch('select id, name from roles')
    print(rows)
    await conn.close()

if __name__ == '__main__':
    asyncio.run(main())
