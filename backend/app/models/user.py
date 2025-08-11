from sqlalchemy import Column, String, Boolean, Integer, Enum
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.common import CommonModel
from app.utils.constant.globals import UserRole
from sqlalchemy.orm import relationship


class User(CommonModel):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True, index=True, autoincrement=True)
	email = Column(String, unique=True, index=True)
	password = Column(String)
	first_name = Column(String, nullable=True)
	last_name = Column(String, nullable=True)
	role = Column(Enum(UserRole), default=UserRole.User)
	phone_number = Column(String, nullable=False)
	is_verified = Column(Boolean, default=False)
	otp_code = Column(String, nullable=True)
	is_deleted = Column(Boolean, default=False)

	def __repr__(self):
		return f"{self.email}"

metadata = Base.metadata

