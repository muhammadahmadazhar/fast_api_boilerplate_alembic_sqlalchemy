from datetime import datetime, timedelta, timezone
from typing import Annotated

from passlib.context import CryptContext
from jose import JWTError, jwt
from sqlalchemy.orm.session import Session

from fastapi import Depends, HTTPException, status

from app.core.dependencies import get_db, oauth2_scheme, pwd_context
from app.core.settings import SECRET_KEY, REFRESH_SECRET_KEY, ALGORITHM
from app.schemas.user import UserCreate
from app.services.user import UserService




class AuthService:

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def authenticate_user(db: Session, user: UserCreate):
        member = UserService.get_user_by_email(db, user.email)
        if not member:
            return False
        if not AuthService.verify_password(user.password, member.password):
            return False
        return member

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
        to_encode.update({"exp": expire})

        to_encode["roles"] = data.get("roles", [])  # Example: ["admin"]

        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    async def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(days=7)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[Session, Depends(get_db)]):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("email")
            roles: list = payload.get("roles", [])

            if not email:
                raise credentials_exception

            user = UserService.get_user_by_email(db, email)
            if not user:
                raise credentials_exception

            user.roles = roles
            user.token = token
            return user

        except JWTError:
            raise credentials_exception