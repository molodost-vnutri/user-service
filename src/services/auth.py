from src.Core import UsersCRUD, UserRolesCRUD
from src.shemas import SUserAuth, SUserInfo
from src.services.psw_ import verify_password
from src.services.jwt_ import JWTCurrentUser
from src.exceptions import MailOrPasswordIncorrect

async def auth_service(body: SUserAuth):
    user_exist = await UsersCRUD.find_one_or_none(email=body.email)
    if not user_exist or not verify_password(password=body.password, hash=user_exist.password):
        raise MailOrPasswordIncorrect
    return JWTCurrentUser.create_access_token(token={'sub': user_exist.id}, days=3)

async def get_current_user_info(user_id: int):
    user = await UsersCRUD.find_by_id(id=user_id)
    roles = await UserRolesCRUD.model_find_all_roles_current_user(user_id=user_id)
    user_dict = {
            "email": user.email,
            "username": user.username,
            "roles": roles,
            "on_create": user.on_create,
            "on_update": user.on_update,
        }
    return SUserInfo(**user_dict)