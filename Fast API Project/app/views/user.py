from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import async_session
from app.schema_validation.userSchema import UserCreate, UserResponse, UserLogin
from app.services.userService import get_user_by_username, create_user
from app.utils.generalUtils import verify_password, create_access_token

router = APIRouter()

async def get_db():
    async with async_session() as session:
        yield session

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    new_user = await create_user(db, user.username, user.email, user.password)
    return new_user

@router.get("/")
async def get_users():
    return {"message": "List of users"}

@router.post("/login")
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_username(db, user.username)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}