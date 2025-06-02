from pydantic import BaseModel, EmailStr, constr

class UserBase(BaseModel):
    email: EmailStr
    username: str
    college: str | None = None

class UserCreate(UserBase):
    password: constr(min_length=12)

class UserResponse(UserBase):
    id: str
    created_at: str

    class Config:
        from_attributes = True