from fastapi import Depends, HTTPException
from typing import List

from app.models import user as UserModel
from app.services.auth import AuthService


class RoleChecker:
    """Dependency class to check user roles."""

    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: UserModel = Depends(AuthService.get_current_user)):
        """Check if user has the required role."""

        # Convert Enum to string
        user_role = str(current_user.role.value) if hasattr(current_user.role, 'value') else str(current_user.role)

        print(f"User Role: {user_role} | Allowed Roles: {self.allowed_roles}")

        if user_role not in self.allowed_roles:
            raise HTTPException(status_code=403, detail="Access forbidden")
