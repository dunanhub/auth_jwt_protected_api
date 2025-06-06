from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.auth import get_current_user, authenticate_user, register_user, create_access_token
from app.models import User
from app.schemas import UserOut

router = APIRouter()

@router.post("/register", response_model=UserOut)
async def register(from_data: OAuth2PasswordRequestForm = Depends()):
    user = await register_user(from_data.username, from_data.password)
    return user

@router.post("/login")
async def login(from_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(from_data.username, from_data.password)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=UserOut)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user