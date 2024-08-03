from src.settings import settings
from src.CRUD import UsersCRUD
from src.shemas import JWTUserChangeEmail, SUserChange_Origin_mail, SMailSend, SUserChangePassword
from src.exceptions import PasswordIncorrect, PasswordNotCorrect, UserAlreadyExist
from src.services.jwt_ import JWTChangeMail
from src.services.psw_ import verify_password, depend_password, hashed_password
from src.Core import send

def change_text_first(token: str) -> str:
    return f'''Вы действительно хотите изменить почту?
Мы не настаиваем изменять её, просто после этого аккаунт не будет никак связан с этой почтой кроме как писем которые там находились.
Но если вы всё таки настроенны серьёзно, то вот держите, но потом не плачьте, что у вас украли аккаунт, придётся писать в тех поддержку чтобы восстановить аккаунт
{settings.HOST}/verify/mail/{token.strip()}
'''

async def update_username_service(username: str, user_id: int):
    if await UsersCRUD.find_one_or_none(username=username):
        raise UserAlreadyExist
    await UsersCRUD.model_update(id=user_id, username=username)

async def send_change_email_first(body: SUserChange_Origin_mail, user_id: int):
    user = await UsersCRUD.find_by_id(id=user_id)
    if not verify_password(password=body.password, hash=user.password):
        raise PasswordIncorrect
    token = JWTChangeMail.create_access_token({'new_email': body.new_email, 'user_id': user_id, 'update': 0}, minutes=15)
    send(
        SMailSend(
            email=user.email,
            subject='Изменение почты',
            message=change_text_first(token)
        )
    )

async def verify_first_change(token: SUserChange_Origin_mail, user_id: int):
    token = JWTChangeMail.decode_token(token=token)
    if token.user_id != user_id:
        return {'msg': 'Пользователь не действителен'}
    token = JWTChangeMail.create_access_token({'new_email': token.new_email, 'user_id': user_id, 'update': 1}, minutes=15)
    send(
        SMailSend(
            email=token.new_email,
            subject='Изменение почты',
            message=f'Ссылка на изменение почты {settings.HOST}/verify/mail/{token}'
        )
    )

async def verify_last_change(token: JWTUserChangeEmail, user_id: int):
    if token.user_id != user_id:
        return {'msg': 'Пользователь не действителен'}
    await UsersCRUD.model_update(id=user_id, email=token.new_email)

async def verify_select(token: str, user_id: int):
    token: JWTUserChangeEmail = JWTUserChangeEmail.decode_token(token)
    match token.update:
        case 0:
            return await verify_first_change(token=token, user_id=user_id)
        case 1:
            return await verify_last_change(token=token, user_id=user_id)

async def change_password(body: SUserChangePassword, user_id: int):
    depend_password(password=body.new_password)
    if body.new_password == body.old_password:
        raise PasswordNotCorrect
    user = await UsersCRUD.find_by_id(id=user_id)
    if not user:
        return {'msg': 'Пользователь не действителен'}
    if not verify_password(password=body.old_password, hash=user.password):
        raise PasswordIncorrect
    password = hashed_password(password=body.new_password)
    await UsersCRUD.model_update(id=user_id, password=password)