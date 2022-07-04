from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    email: EmailStr

    
class UserCreate(UserBase):
    password: str


class UserLogin(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class JD(BaseModel):
    wd_id: int
    position: str
    main_tasks: str
    requirements: str
    preferred_points: str