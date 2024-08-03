from src.services.jwt_ import JWTVerify
from src.Core import send
from src.settings import settings
from src.services.psw_ import depend_password, hashed_password
from src.shemas import SUserAddPasswod, SUserCreate, SMailSend
from src.CRUD import UsersCRUD, UserRolesCRUD

def verify_text(token: str) -> str:
    return f'''Тук-тук к вам пришли чтобы вы дали согласие на регистрацию аккаунта
Мы не настаиваем на согласия, просто после этого вы сможете слушать свою любимую музыку без рекламы, но если вы не подавали запрос на регистрацию, то не стоит регистрироваться пока не узнаете о чём речь.
{settings.HOST}/verify/mail/{token}
Если вы не отправляли запрос на регистрацию, то можете посмотреть что упускаете https://{settings.HOST}/docs
'''

async def send_registration_link(body: SUserCreate):
    if await UsersCRUD.find_one_or_none(email=body.email):
        return
    token = JWTVerify.create_access_token(token={'email': body.email}, minutes=15)
    send(
        SMailSend(
            email=body.email,
            subject='Завершение регистрации пользователя',
            message=verify_text(token)
        )
    )
async def verify_token(token: str, body: SUserAddPasswod):
    token = JWTVerify.decode_token(token)
    depend_password(password=body.password, password_verify=body.password_verify)
    password = hashed_password(password=body.password)
    user_id = await UsersCRUD.model_add(email=token.email, password=password)
    
    await UserRolesCRUD.model_add(user_id=user_id, role='Пользователь')