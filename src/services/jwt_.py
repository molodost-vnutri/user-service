from src.Core import BaseJWT
from src.shemas import JWTCurrentUser, JWTUserChangeEmail, JWTCreateMail

class JWTVerify(BaseJWT):
    schemas_validator = JWTCreateMail

class JWTCurrentUser(BaseJWT):
    schemas_validator = JWTCurrentUser

class JWTChangeMail(BaseJWT):
    schemas_validator = JWTUserChangeEmail