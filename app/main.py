from fastapi import FastAPI

from app.api.v1 import auth, books, categories, users, borrowings, reservations, dashboard
from app.core.config import settings

app = FastAPI(
    title="Limkokwing Library Management API",
    description="RESTful API for library operations at Limkokwing University.",
    version="1.0.0",
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(categories.router, prefix="/api/v1/categories", tags=["Categories"])
app.include_router(books.router, prefix="/api/v1/books", tags=["Books"])
app.include_router(borrowings.router, prefix="/api/v1/borrowings", tags=["Borrowings"])
app.include_router(reservations.router, prefix="/api/v1/reservations", tags=["Reservations"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["Dashboard"])

@app.get("/health", summary="Health check")
async def health_check() -> dict[str, str]:
    return {"status": "ok", "environment": settings.environment}
