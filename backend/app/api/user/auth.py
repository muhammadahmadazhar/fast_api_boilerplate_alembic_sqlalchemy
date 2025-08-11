from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from datetime import timedelta

# sqlalchemy
from sqlalchemy.orm import Session
from app.core.role_checker import RoleChecker

# import
from app.schemas.user import User, UserLogin, Token, PasswordUpdate
from app.core.dependencies import get_db
from app.core.settings import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from app.services.auth import AuthService
from app.services.user import UserService
from app.utils.constant.globals import generate_signed_url

auth_module = APIRouter()


# ============> login/logout < ======================
# getting access token for login
@auth_module.post("/login", response_model=Token)
async def login_for_access_token(
    user: UserLogin, db: Session = Depends(get_db)
) -> Token:
    # Authenticate user
    member = AuthService.authenticate_user(db, user=user)
    if not member:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if member.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are account id Deleted, please Contact admin for assistance.",
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = AuthService.create_access_token(
        data={
            "id": member.id,
            "email": member.email,
            "role": member.role,
            "isVerified": member.is_verified,
            # "isActive": member.is_active,
            # "isFirstLogin": is_first_login,
            # "isPaymentCompleted": is_payment_completed,
            # "isAccountApproved": is_account_approved,
        },
        expires_delta=access_token_expires,
    )

    # Fetch current user
    user = AuthService.get_current_user(access_token, db)
    # if not user.is_verified:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Please verify your email before logging in again.",
    #     )

    # Generate refresh token
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = await AuthService.create_refresh_token(
        data={"id": member.id, "email": member.email, "role": member.role},
        expires_delta=refresh_token_expires,
    )

    # Create a structured User response
    user_response = User(
        id=user.id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        role=user.role,
        phone_number=user.phone_number,
        created_at=user.created_at,
        updated_at=user.updated_at,
        is_verified=user.is_verified,
        access_token=access_token,
    )

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        data=user_response,
    )


# @auth_module.post("/refresh", response_model=Token)
# async def refresh_access_token(refresh_token: str, db: Session = Depends(get_db)):
#     token = await refresh_access_token(db, refresh_token)
#     return token


# @auth_module.get("/users/me/", response_model=User)
# async def read_current_user(
#     current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
# ):
#     # Get profile picture based on user role
#     profile_picture = None
#     approval = None
#
#     if current_user.role in [UserRole.THERAPIST, UserRole.ADMIN]:
#         therapist = (
#             db.query(Therapist).filter(Therapist.user_id == current_user.id).first()
#         )
#
#         if therapist:
#             profile_picture = therapist.profile_picture
#             approval = TherapistApproval(
#                 is_first_login=therapist.is_first_login,
#                 is_account_approved=therapist.is_account_approved,
#                 is_payment_completed=therapist.is_payment_completed,
#                 is_rejected=therapist.is_rejected,
#             )
#         else:
#             approval = TherapistApproval(
#                 is_first_login=True,
#                 is_account_approved=False,
#                 is_payment_completed=False,
#             )
#     elif current_user.role == UserRole.CLIENT:
#         client = db.query(Client).filter(Client.user_id == current_user.id).first()
#         if client:
#             profile_picture = client.profile_picture
#
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     new_access_token = create_access_token(
#         data={
#             "id": current_user.id,
#             "email": current_user.email,
#             "role": current_user.role,
#             "isVerified": current_user.is_verified,
#             "isActive": current_user.is_active,
#             "isAccountApproved": approval.is_account_approved if approval else False,
#             "isFirstLogin": approval.is_first_login if approval else False,
#             "isPaymentCompleted": approval.is_payment_completed if approval else False,
#         },
#         expires_delta=access_token_expires,
#     )
#
#     user_response = User(
#         id=current_user.id,
#         email=current_user.email,
#         first_name=current_user.first_name,
#         last_name=current_user.last_name,
#         is_active=current_user.is_active,
#         role=current_user.role,
#         phone_number=current_user.phone_number,
#         created_at=current_user.created_at,
#         updated_at=current_user.updated_at,
#         is_verified=current_user.is_verified,
#         access_token=new_access_token,
#         approval=approval,
#         profile_picture=generate_signed_url(profile_picture),
#     )
#     return user_response
#
#
# @auth_module.put("/users/update-password", response_model=dict)
# async def update_password(
#     password_update: PasswordUpdate,
#     current_user: User = Depends(get_current_user),
#     db: Session = Depends(get_db),
# ):
#     """
#     Update the user's password after verifying the old password.
#     """
#
#     if not current_user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
#         )
#
#     if not verify_password(password_update.old_password, current_user.password):
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, detail="Old password is incorrect"
#         )
#
#     hashed_password = hash_password(password_update.new_password)
#
#     current_user.password = hashed_password
#     db.commit()
#     db.refresh(current_user)
#
#     return {"message": "Password updated successfully"}
