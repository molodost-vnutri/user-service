from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

#Авторизация пользователя

class SUserAuth(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=32)

#Регистрация пользователя

class SUserCreate(BaseModel):
    email: EmailStr

class SUserAddPasswod(BaseModel):
    password: str = Field(min_length=8, max_length=32)
    password_verify: str = Field(min_length=8, max_length=32)

#Смена юзернейма

class SUserChangeUsername(BaseModel):
    username: str = Field(min_length=4, max_length=20)

#Смена пароля

class SUserChangePassword(BaseModel):
    old_password: str
    new_password: str = Field(min_length=8, max_length=32)

#Смена почты

#Валидация пароля и получение новой почты
class SUserChange_One(BaseModel):
    new_email: EmailStr
    password: str

#Получение новой почты
class SUserChange_Two(BaseModel):
    new_email: EmailStr

#Создание схемы письма
class SendMail(BaseModel):
    email: EmailStr
    subject: str
    message: str

class SUserInfo(BaseModel):
    email: EmailStr
    username: None | str
    roles: list[str]
    on_create: datetime
    on_update: datetime

#JWT схемы

class SJWTExpire(BaseModel):
    exp: float

class SVJWTcurrentUser(SJWTExpire):
    sub: int

class SVJWT(SJWTExpire):
    email: EmailStr

class SUserChangeEmailJWT(SUserChange_Two):
    user_id: int

class SVUserChangeEmailJWT(SUserChangeEmailJWT, SJWTExpire):
    update: int