from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlmodel import select
from app.models import User
from app.database import async_session
from dotenv import load_dotenv
import os

load_dotenv()

SECRETE_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_ecode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_ecode.update({"exp": expire})
    return jwt.encode(to_ecode, SECRETE_KEY, algorithm=ALGORITHM)

async def register_user(username: str, password: str):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.username == username))
        exitsting_user = result.first()
        if exitsting_user:
            raise HTTPException(
                status_code=401,
                detail="Username already exists"
            )
        hashed_password = get_password_hash(password)
        user = User(username=username, password=hashed_password)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
    
async def authenticate_user(username: str, password: str):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.username == username))
        user = result.scalars().first()
        if not user or not verify_password(password, user.password):
            return None
        return user

async def verify_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRETE_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception

async def get_current_user(username: str = Depends(verify_token)):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.username == username))
        user = result.scalars().first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user