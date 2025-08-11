import os
from dotenv import load_dotenv

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.core.dependencies import get_db, oauth2_scheme
# from app.core.role_checker import RoleChecker
# from app.schemas.therapist import ResetPasswordRequest, ForgotPasswordRequest
from app.schemas.user import User, UserCreate #, UserUpdate, OTPVerificationRequest, InviteRequest, AdminResponseSchema, \
    # AdminUpdateSchema

from app.services.user import UserService
from app.utils.constant.globals import send_email_reset_link, send_invite_email

user_module = APIRouter()
load_dotenv()


# # create new user
@user_module.post('/signup', response_model=User)
async def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = UserService.get_user_by_email(db, user.email)

    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")
    new_user = UserService.create_new_user(db, user)
    return new_user
#
# @user_module.post("/verify-otp")
# async def verify_user(request: OTPVerificationRequest, db: Session = Depends(get_db)):
#     user = user_functions.get_user_by_email(db, request.email)
#
#     if not user or user.otp_code != request.otp:
#         raise HTTPException(status_code=400, detail="Invalid OTP")
#
#     user.is_verified = True
#     user.otp_code = None
#     db.commit()
#     return {"message": "User verified successfully"}
#
# @user_module.get('/', response_model=list[User],
#             # dependencies=[Depends(RoleChecker(['admin']))]
#             )
# async def read_all_user( skip: int = 0, limit: int = 100,  db: Session = Depends(get_db)):
#     return user_functions.read_all_user(db, skip, limit)
#
# @user_module.post("/forgot-password")
# async def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
#     user = user_functions.get_user_by_email(db, request.email)
#
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#
#     token = user_functions.generate_reset_token(user.email)
#
#     reset_link = f"{os.getenv('DOMAIN')}/reset-password?token={token}"
#
#     print(f"Password reset link for {request.email}: {reset_link}")
#     send_email_reset_link(request.email, reset_link)
#
#     return {"message": "Password reset link sent to your email"}
#
# @user_module.get("/verify-reset-token")
# async def verify_reset_token_route(token: str):
#     email = user_functions.verify_reset_token(token)
#     return {"message": "Token verified. Redirect user to reset password page", "email": email}
#
# @user_module.post("/reset-password")
# async def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
#     try:
#         email = user_functions.verify_reset_token(request.token)
#     except Exception:
#         raise HTTPException(status_code=400, detail="Invalid or expired token")
#
#     user = user_functions.get_user_by_email(db, email)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#
#     new_hash = user_functions.hash_password(request.new_password)
#     user.password = new_hash
#     db.add(user)
#     db.commit()
#     db.refresh(user)
#
#     return {"message": "Password reset successfully"}
#
# @user_module.post("/send-invite", dependencies=[Depends(RoleChecker(['admin']))])
# async def send_invite(request: InviteRequest,
#                       db: Session = Depends(get_db),
#                       ):
#     existing_user = get_user_by_email(db, request.email)
#     if existing_user:
#         raise HTTPException(status_code=400, detail="User with this email already exists")
#
#     INVITE_URL = os.getenv("DOMAIN")
#     send_invite_email(request.email, f"{INVITE_URL}/login")
#     return {"message": f"Invitation sent to {request.email}"}
#
# @user_module.get('/admin/{user_id}', response_model=AdminResponseSchema,
#             # dependencies=[Depends(RoleChecker(['admin']))]
#             )
# async def read_admin_by_id( user_id: int, db: Session = Depends(get_db)):
#     return user_functions.get_admin_by_id(db, user_id)
#
#
# @user_module.put("/admin/{user_id}")
# def update_admin(user_id: int, payload: AdminUpdateSchema, db: Session = Depends(get_db)):
#     return user_functions.update_admin_details(user_id, payload, db)
#
# @user_module.get('/{user_id}', response_model=User,
#             # dependencies=[Depends(RoleChecker(['admin']))]
#             )
# async def read_user_by_id( user_id: int, db: Session = Depends(get_db)):
#     return user_functions.get_user_by_id(db, user_id)
#
# # update user
# @user_module.patch('/{user_id}', response_model=User,
#             #   dependencies=[Depends(RoleChecker(['admin']))]
#               )
# async def update_user( user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
#     print(f"Received data: {user.model_dump()}")
#     return user_functions.update_user(db, user_id, user)
#
# # delete user
# @user_module.delete('/{user_id}',
#                dependencies=[Depends(RoleChecker(['admin']))]
#                )
# async def delete_user( user_id: int, db: Session = Depends(get_db)):
#     return user_functions.soft_delete_user(db, user_id)
#
#
