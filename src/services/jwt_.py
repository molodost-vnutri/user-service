from src.Core import BaseJWT
from src.shemas import SUserCreate, SVJWT, SVJWTcurrentUser, SUserChangeEmailJWT, SVUserChangeEmailJWT



class JWTVerify(BaseJWT):
    schemas_create = SUserCreate
    schemas_validator = SVJWT

class JWTCurrentUser(BaseJWT):
    schemas_create = SVJWTcurrentUser

class JWTEmailChange(BaseJWT):
    schemas_create = SUserChangeEmailJWT
    schemas_validator = SVUserChangeEmailJWT