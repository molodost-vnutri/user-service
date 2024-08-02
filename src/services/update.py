from src.settings import settings
from src.Core import UsersCRUD
from src.shemas import SUserChangeEmailJWT, SUserChange_One, SVUserChangeEmailJWT
from src.exceptions import PasswordIncorrect
from src.services.jwt_ import JWTEmailChange
from src.services.psw_ import verify_password
from src.Core import MailBase, SendMail 



def change_text_first(token: str) -> str:
    return f'''Вы действительно хотите изменить почту?
Мы не настаиваем изменять её, просто после этого аккаунт не будет никак связан с этой почтой кроме как писем которые там находились.
Но если вы всё таки настроенны серьёзно, то вот держите, но потом не плачьте, что у вас украли аккаунт, придётся писать в тех поддержку чтобы восстановить аккаунт
{settings.HOST}/verify/mail/{token}'''

async def update_username_service(username: str, user_id: int):
    await UsersCRUD.model_update(id=user_id, username=username)

async def send_change_email_first(body: SUserChange_One, user_id: int):
    user = await UsersCRUD.find_by_id(id=user_id)
    if not verify_password(password=body.password, hash=user.password):
        raise PasswordIncorrect
    token = JWTEmailChange.create_access_token({'new_email': body.new_email, 'user_id': user_id, 'update': 0}, minutes=15)
    MailBase.send(
        SendMail(
            email=user.email,
            subject='Изменение почты',
            message=change_text_first(token)
        )
    )

async def verify_first_change(token: SVUserChangeEmailJWT, user_id: int):
    token: SUserChangeEmailJWT = JWTEmailChange.decode_token(token=token)
    if token.user_id != user_id:
        return {'msg': 'Пользователь не действителен'}
    token = JWTEmailChange.create_access_token({'new_email': token.new_email, 'user_id': user_id, 'update': 1}, minutes=15)
    MailBase.send(
        SendMail(
            email=token.new_email,
            subject='Изменение почты',
            message=f'Ссылка на изменение почты {settings.HOST}/verify/mail/{token}'
        )
    )

async def verify_last_change(token: SVUserChangeEmailJWT, user_id: int):
    if token.user_id != user_id:
        return {'msg': 'Пользователь не действителен'}
    await UsersCRUD.model_update(id=user_id, email=token.new_email)

async def verify_select(token: str, user_id: int):
    token: SVUserChangeEmailJWT = JWTEmailChange.decode_token(token)
    match token.update:
        case 0:
            return await verify_first_change(token=token, user_id=user_id)
        case 1:
            return await verify_last_change(token=token, user_id=user_id)