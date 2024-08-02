from fastapi import Request, Depends

from src.services.jwt_ import JWTCurrentUser
from src.exceptions import TokenNotFound

def get_token(response: Request):
    try:
        return response.cookies.get('access_token')
    except:
        raise TokenNotFound

def get_current_user(token = Depends(get_token)):
    return JWTCurrentUser.decode_token(token)