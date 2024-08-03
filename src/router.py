from fastapi import APIRouter, Depends, Response

from src.services.dependencies import delete_cookies, get_current_user, check_user_auth
from src.services.auth import auth_service
from src.services.user_info import get_current_user_info
from src.services.update import update_username_service, send_change_email_first, verify_select, change_password
from src.services.create import send_registration_link, verify_token
from src.shemas import SUserChange_Origin_mail, SUserAuth, SUserChangeUsername, SUserCreate, SUserChangePassword, SUserAddPasswod, JWTCurrentUser

router = APIRouter(
    prefix='/profile',
    tags=['Авторизация и пользователи']
)

@router.post('', status_code=200)
async def send_mail_registration(body: SUserCreate, _ = Depends(check_user_auth)):
    await send_registration_link(body=body)
    return {'msg': 'Если пользователь ещё не зарегистрирован, то письмо будет отправлено на почту'}

@router.post('/auth', status_code=200)
async def auth_user(body: SUserAuth, response: Response, _ = Depends(check_user_auth)):
    token = await auth_service(body=body)
    response.set_cookie('access_token', token, httponly=True)
    return {'msg': token}

@router.post('/verify/email/{token}', status_code=201)
async def success_verify_mail(token: str, body: SUserAddPasswod, _ = Depends(check_user_auth)):
    await verify_token(token=token, body=body)
    return {'msg': 'Пользователь верифицирован'}

@router.patch('/change/username', status_code=200)
async def change_username(username: SUserChangeUsername, user_id: JWTCurrentUser = Depends(get_current_user)):
    await update_username_service(user_id=user_id.sub, username=username.username)
    return {'msg': 'Юзернейм успешно изменён'}

@router.patch('/change/email', status_code=200)
async def change_email(body: SUserChange_Origin_mail, user_id: JWTCurrentUser = Depends(get_current_user)):
    result = await send_change_email_first(body=body, user_id=user_id.sub)
    if result: return Depends(delete_cookies)
    return {'msg': 'Письмо с ссылкой отправлено на оригинальную почту'}

@router.patch('/change/password', status_code=200)
async def change_password(body: SUserChangePassword, user_id: JWTCurrentUser = Depends(get_current_user)):
    result = await change_password(body=body, user_id=user_id.sub)
    del_cook = Depends(delete_cookies)
    if result: return del_cook
    return {'msg': 'Пароль успешно изменён'}


@router.get('/verify/email/{token}', status_code=200)
async def verify_token_change(token: str, user_id: JWTCurrentUser = Depends(get_current_user)):
    result = await verify_select(token=token, user_id=user_id.sub)
    if result: return Depends(delete_cookies)
    return {'msg': 'OK'}

@router.get('/info', status_code=200)
async def get_user_info(user_id: JWTCurrentUser = Depends(get_current_user)):
    return await get_current_user_info(user_id=user_id.sub)