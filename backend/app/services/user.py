from sqlalchemy.orm import Session

# from auth import models, schemas
from passlib.context import CryptContext
from jose import JWTError, jwt

from app.utils.constant.globals import generate_otp, send_email_otp, UserRole, generate_signed_url
# import
from app.models import user as UserModel
from app.schemas.user import UserCreate, UserUpdate, Token, AdminSchema, LocationSchema, AdminResponseSchema, \
    AdminUpdateSchema
from app.core.settings import SECRET_KEY, REFRESH_SECRET_KEY, ALGORITHM
from app.core.settings import ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.dependencies import get_db, oauth2_scheme
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, FastAPI, HTTPException, status

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:

    @staticmethod
    def create_new_user(db: Session, user: UserCreate):
        # otp = generate_otp()
        role = user.role if user.role else UserRole.User
        hashed_password = pwd_context.hash(user.password)
        new_user = UserModel.User(email=user.email, password=hashed_password, first_name=user.first_name,
                                  last_name=user.last_name, phone_number=user.phone_number,
                                  # otp_code=otp,
                                  role=role)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        # send_email_otp(user.email, otp)
        return new_user

    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return db.query(UserModel.User).filter(UserModel.User.email == email).first()