from src.shemas import SUserInfo
from src.CRUD import UsersCRUD, UserRolesCRUD

async def get_current_user_info(user_id: int):
    user = await UsersCRUD.find_by_id(id=user_id)
    roles = await UserRolesCRUD.model_find_all_roles_current_user(user_id=user_id)
    user_dict = {
        'email': user.email,
        'username': user.username,
        'roles': roles,
        'on_create': user.on_create,
        'on_update': user.on_update
    }
    return SUserInfo(**user_dict)