import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.v1 import auth, books, categories, users, borrowings, reservations, dashboard
from app.core.config import settings

logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.DEBUG if settings.debug else logging.INFO)

app = FastAPI(
    title="Limkokwing Library Management API",
    description="RESTful API for library operations at Limkokwing University.",
    version="1.0.0",
    debug=settings.debug,
)

@app.middleware("http")
async def log_exceptions(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        logger.exception("Unhandled exception while processing request")
        raise

@app.exception_handler(Exception)
async def internal_server_error_handler(request: Request, exc: Exception):
    logger.exception("Internal server error")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error. Check server logs for details."},
    )

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(categories.router, prefix="/api/v1/categories", tags=["Categories"])
app.include_router(books.router, prefix="/api/v1/books", tags=["Books"])
app.include_router(borrowings.router, prefix="/api/v1/borrowings", tags=["Borrowings"])
app.include_router(reservations.router, prefix="/api/v1/reservations", tags=["Reservations"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["Dashboard"])

@app.get("/", summary="Root")
async def root() -> dict[str, str]:
    return {
        "message": "Welcome to Limkokwing Library Management API"
    }


@app.get("/health", summary="Health check")
async def health_check() -> dict[str, str]:
    return {"status": "ok", "environment": settings.environment}

