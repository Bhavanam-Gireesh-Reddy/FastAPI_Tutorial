from pydantic import BaseModel, EmailStr

# Schema for new user creation
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str

# Schema for user login
class UserLogin(BaseModel):
    username: str
    password: str