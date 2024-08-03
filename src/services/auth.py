from src.CRUD import UsersCRUD
from src.shemas import SUserAuth
from src.services.jwt_ import JWTCurrentUser
from src.services.psw_ import verify_password
from src.exceptions import MailOrPasswordIncorrect

async def auth_service(body: SUserAuth):
    user_exist = await UsersCRUD.find_one_or_none(email=body.email)
    if not user_exist or not verify_password(password=body.password, hash=user_exist.password):
        raise MailOrPasswordIncorrect
    return JWTCurrentUser.create_access_token(token={'sub': user_exist.id}, days=3)