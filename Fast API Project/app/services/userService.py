import uuid
from uuid import UUID

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from app.models.userModel import User, UserInfo
from app.schema_validation.userSchema import UserDetailsCreate
from app.utils.generalUtils import get_password_hash, verify_token


async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, username: str, email: str, password: str):
    hashed_password = get_password_hash(password)
    new_user = User(
        username=username,
        email=email,
        hashed_password=hashed_password
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def create_user_details(db: AsyncSession, user_data: UserDetailsCreate, user_id: UUID):
    new_user_details = UserInfo(
        firstName=user_data.firstName,
        lastName=user_data.lastName,
        mobileNumber=user_data.mobileNumber,
        city=user_data.city,
        state=user_data.state,
        pincode=user_data.pincode,
        user_id=user_id
    )

    db.add(new_user_details)
    await db.commit()
    await db.refresh(new_user_details)
    return new_user_details


async def get_current_user(token: str, db: AsyncSession):
    username = verify_token(token)
    async with db.begin():
        result = await db.execute(select(User).filter(User.username == username))
        db_user = result.scalars().first()

    if db_user is None:
        raise HTTPException(status_code=400, detail="User not found")

    return db_user

async def check_user_info(user_id: uuid.UUID, db: AsyncSession):
    result = await db.execute(select(UserInfo).filter(UserInfo.user_id == user_id))
    return result.scalars().first()

async def update_user_details(db: AsyncSession, user_info: UserInfo, user_details: UserDetailsCreate):
    user_info.firstName = user_details.firstName
    user_info.lastName = user_details.lastName
    user_info.mobileNumber = user_details.mobileNumber
    user_info.city = user_details.city
    user_info.state = user_details.state
    user_info.pincode = user_details.pincode

    await db.commit()
    await db.refresh(user_info)
    return user_info