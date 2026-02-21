from pydantic import BaseModel, EmailStr


#schemas for user registration and login
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str

#schemas for user login
class UserLogin(BaseModel):
    username: str
    password: str