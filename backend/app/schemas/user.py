from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List
from app.utils.constant.globals import UserRole


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None
    role: Optional[UserRole] = None


class UserLogin(UserBase):
    password: str


class User(UserBase):
    id: int
    first_name: Optional[str]
    last_name: Optional[str]
    # is_active: bool
    role: UserRole or None
    phone_number: str
    created_at: datetime
    updated_at: datetime
    is_verified: bool
    access_token: Optional[str] = None
    # approval: Optional[TherapistApproval] = None
    profile_picture: Optional[str] = None

    class Config:
        from_attributes = True
        orm_mode = True


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    is_active: bool | None = None
    role: UserRole or None = None


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    data: Optional[User]


class OTPVerificationRequest(BaseModel):
    email: str
    otp: str


class InviteRequest(BaseModel):
    email: EmailStr


class PasswordUpdate(BaseModel):
    old_password: str = Field(..., min_length=6, max_length=100)
    new_password: str = Field(..., min_length=6, max_length=100)


class LocationSchema(BaseModel):
    id: int
    street: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zip_code: Optional[str]
    country: Optional[str]

    class Config:
        orm_mode = True
        from_attributes = True


class AdminSchema(BaseModel):
    id: int
    user_id: int
    appointment_type: Optional[str]
    ethnicity: Optional[str]
    gender: Optional[str]
    age: Optional[str]
    faith: Optional[str]
    bio: Optional[str]
    sexuality: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    phone_number: Optional[str]
    email: EmailStr
    relationship_status: Optional[str]
    profile_picture: Optional[str]

    class Config:
        from_attributes = True
        orm_mode = True


class AdminResponseSchema(BaseModel):
    therapist: AdminSchema
    locations: List[LocationSchema]

    class Config:
        from_attributes = True
        orm_mode = True


class LocationUpdateSchema(BaseModel):
    id: Optional[int]
    city: Optional[str]
    zip_code: Optional[str]
    country: Optional[str]

    class Config:
        orm_mode = True


class AdminUpdateSchema(BaseModel):
    gender: Optional[str] = None
    age: Optional[str] = None
    faith: Optional[str] = None
    address_type: Optional[str] = "Home"
    bio: Optional[str] = None
    sexuality: Optional[str] = None
    relationship_status: Optional[str] = None
    locations: Optional[List[LocationUpdateSchema]] = None

    class Config:
        orm_mode = True
