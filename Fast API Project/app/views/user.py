import logging

from fastapi import APIRouter, Depends, HTTPException, status, Header, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import async_session
from app.schema_validation.userSchema import UserCreate, UserResponse, UserLogin, UserDetailsCreate
from app.services.userService import get_user_by_username, create_user, create_user_details, get_current_user, \
    check_user_info, update_user_details
from app.utils.generalUtils import verify_password, create_access_token, create_refresh_token, generate_otp
from fastapi.security import OAuth2PasswordBearer
from twilio.rest import Client

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
    message = "List of users"
    logger.info("Log message %s", message)
    return {"message": message}

@router.get("/send_otp")
async def otp_mobilenumber(account_sid: str, auth_token: str, to_number: str):
    client = Client(account_sid, auth_token)
    try:
        otp = generate_otp()
        message_body = f"Harshini Service - {otp} is your verification code for secure access"
        message = client.messages.create(
            from_='+18649774597',
            body=message_body,
            to=to_number
        )
        return {"message_sid": message.sid, "status": "Message sent successfully"}
    except Exception as e:
        return {"error": str(e), "status": "Failed to send message"}

@router.post("/login")
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_username(db, user.username)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": db_user.username})
    refresh_token = create_refresh_token(data={"sub": db_user.username})
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/user_details")
async def save_user_details(
        user: UserDetailsCreate,
        db: AsyncSession = Depends(get_db),
        authorization: str = Header(None)
        ):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    token = authorization
    current_user = await get_current_user(token, db)
    if current_user is None:
        raise HTTPException(status_code=401, detail="User not found")

    existing_user_info = await check_user_info(current_user.id, db)

    if existing_user_info:
        updated_user_info = await update_user_details(db, existing_user_info, user)
        return {"message": "User details updated successfully", "user_info": updated_user_info}
    else:
        new_user_info = await create_user_details(db, user, current_user.id)
        return {"message": "User details created successfully", "user_info": new_user_info}