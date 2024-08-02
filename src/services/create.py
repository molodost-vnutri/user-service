from src.services.jwt_ import JWTVerify
from src.Core import MailBase
from src.settings import settings
from src.services.psw_ import depend_password, hashed_password
from src.shemas import SUserAddPasswod, SUserCreate, SendMail
from src.Core import UsersCRUD, UserRolesCRUD

def verify_text(token: str) -> str:
    return f'''Вы действительно хотите изменить почту?
Мы не настаиваем изменять её, просто после этого аккаунт не будет никак связан с этой почтой кроме как писем которые там находились.
Но если вы всё таки настроенны серьёзно, то вот держите, но потом не плачьте, что у вас украли аккаунт, придётся писать в тех поддержку чтобы восстановить аккаунт
{settings.HOST}/verify/mail/{token}
'''

def send_registration_link(body: SUserCreate):
    token = JWTVerify.create_access_token(token={'email': body.email}, minutes=15)
    MailBase.send(
        SendMail(
            email=body.email,
            subject='Завершение регистрации пользователя',
            message=verify_text(token)
        )
    )
async def vefify_token(token: str, body: SUserAddPasswod):
    token = JWTVerify.decode_token(token)
    depend_password(password=body.password, password_verify=body.password_verify)
    password = hashed_password(password=body.password)
    user_id = await UsersCRUD.model_add(email=token.email, password=password)
    
    await UserRolesCRUD.model_add(user_id=user_id, role='Пользователь')