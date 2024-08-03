from fastapi import Request, Response, Depends

from src.services.jwt_ import JWTCurrentUser
from src.exceptions import TokenNotFound, UserAlreadyAuth

def get_token(response: Request):
    token = response.cookies.get('access_token')
    if token:
        return token

def get_current_user(token = Depends(get_token)):
    if not token:
        raise TokenNotFound
    return JWTCurrentUser.decode_token(token)

def check_user_auth(token = Depends(get_token)):
    if token:
        raise UserAlreadyAuth

def delete_cookies(response: Response):
    response.delete_cookie('access_token')
    return {'Пользователь не найден'}