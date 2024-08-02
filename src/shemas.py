from pydantic import BaseModel, EmailStr, Field

class SUserAuth(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=32)

class SUserFirstCreate(BaseModel):
    email: EmailStr

class SUserSecondCreate(BaseModel):
    password: str = Field(min_length=8, max_length=32)
    password_verify: str = Field(min_length=8, max_length=32)

class SUserChangeUsername(BaseModel):
    username: str = Field(min_length=4, max_length=20)

class SUserChangePassword(BaseModel):
    old_password: str
    new_password: str = Field(min_length=8, max_length=32)

class SUserChangeEmail(BaseModel):
    new_email: EmailStr
    password: str