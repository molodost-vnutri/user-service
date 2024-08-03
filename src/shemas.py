from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

class SUserAuth(BaseModel):
    email: EmailStr
    password: str

class SUserCreate(BaseModel):
    email: EmailStr

class SUserAddPasswod(BaseModel):
    password: str = Field(min_length=8, max_length=32)
    password_verify: str = Field(min_length=8, max_length=32)

class SUserChangeUsername(BaseModel):
    username: str = Field(min_length=4, max_length=20)

class SUserChangePassword(BaseModel):
    old_password: str
    new_password: str = Field(min_length=8, max_length=32)

class SUserChange_Origin_mail(BaseModel):
    new_email: EmailStr
    password: str

class SMailSend(BaseModel):
    email: EmailStr
    subject: str
    message: str

class SUserInfo(BaseModel):
    email: EmailStr
    username: None | str
    roles: list[str]
    on_create: datetime
    on_update: datetime

class JWTExpire(BaseModel):
    exp: float

class JWTCurrentUser(JWTExpire):
    sub: int

class JWTCreateMail(JWTExpire):
    email: EmailStr

class JWTUserChangeEmail(JWTExpire):
    update: int
    new_email: EmailStr
    user_id: int