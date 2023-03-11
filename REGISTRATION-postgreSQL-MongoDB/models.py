from typing import Optional

from pydantic import BaseModel, EmailStr


# User registration request body
class UserRegistration(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    phone: Optional[str] = None
    profile_picture: Optional[str] = None


# User data model for PostgreSQL
class UserPostgres(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    phone: Optional[str] = None


# User data model for MongoDB
class UserProfilePictureMongoDB(BaseModel):
    id: str
    profile_picture: str
