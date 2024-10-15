from pydantic import BaseModel, EmailStr
from uuid import UUID

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserDetailsCreate(BaseModel):
    firstName: str
    lastName: str
    mobileNumber: str
    city: str
    state: str
    pincode: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: UUID
    username: str
    email: EmailStr

    class Config:
        orm_mode = True
