from fastapi import APIRouter

from src.shemas import SUserFirstCreate

router = APIRouter(
    prefix='profile',
    tags=['Авторизация и пользователи']
)

@router.post('', status_code=201)
async def send_mail_registration(body: SUserFirstCreate):
    pass