from fastapi import APIRouter

router = APIRouter()


@router.post("/register", summary="Register a new user")
async def register():
    return {"message": "Register endpoint placeholder"}


@router.post("/login", summary="Authenticate a user")
async def login():
    return {"message": "Login endpoint placeholder"}
