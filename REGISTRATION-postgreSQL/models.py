from pydantic import BaseModel


class UserRegistration(BaseModel):
    full_name: str
    email: str
    password: str
    phone: str
    profile_picture: str


class UserProfile(BaseModel):
    user_id: int
    profile_picture: str
