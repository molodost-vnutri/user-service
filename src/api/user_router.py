from fastapi import APIRouter, Response, Depends, HTTPException

from src.services.dependencies import get_current_user
from src.services.auth import auth_service
from src.services.update import update_username_service, send_change_email_first, verify_select
from src.shemas import SUserChange_One, SUserAuth, SUserChangeUsername, SVJWTcurrentUser, SUserCreate, SUserAddPasswod
from src.services.create import send_registration_link, vefify_token

router = APIRouter(
    prefix='/profile',
    tags=['Авторизация и пользователи']
)

@router.post('', status_code=200)
def send_mail_registration(body: SUserCreate):
    send_registration_link(body)
    return {
        'msg': 'письмо было отправлено на указанную почту'
    }

@router.post('/verify/email/{token}', status_code=201)
async def verify_token(token: str, body: SUserAddPasswod):
    await vefify_token(token=token, body=body)
    return {'msg': 'Пользователь верифицирован'}

@router.post('/auth', status_code=200)
async def auth(body: SUserAuth, response: Response):
    token = await auth_service(body=body)
    response.set_cookie('access_token', token, httponly=True)
    return {'access_token': token}

@router.patch('/change/username', status_code=200)
async def change_username(username: SUserChangeUsername, user_id: SVJWTcurrentUser = Depends(get_current_user)):
    await update_username_service(user_id=user_id.sub, username=username.username)
    return {'msg': 'Юзернейм успешно изменён'}

@router.patch('/change/email', status_code=200)
async def change_email(body: SUserChange_One, response: Response, user_id: SVJWTcurrentUser = Depends(get_current_user)):
    result = await send_change_email_first(body=body, user_id=user_id)
    if result:
        response.delete_cookie('access_token')
        raise HTTPException(
            status_code=404,
            detail=result
        )
    return {'Письмо с ссылкой на подтверждение отправлено на оригинальную почту'}

@router.get('/verify/email/{token}')
async def verify_token(token: str, response: Response, user_id = Depends(get_current_user)):
    result = await verify_select(token=token, user_id=user_id)
    if result:
        response.delete_cookie('access_token')
        return HTTPException(
            status_code=404,
            detail=result
        )
    return 'Ok'