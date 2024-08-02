from re import search

from fastapi import HTTPException
from passlib.context import CryptContext

from src.exceptions import (
    PasswordChar,
    PasswordLowerCase,
    PasswordNotAscii,
    PasswordNotValidCreate,
    PasswordNum,
    PasswordUpperCase
)

psw_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def verify_password(password: str, hash: str) -> bool:
    return psw_context.verify(secret=password, hash=hash)

def hashed_password(password: str) -> str:
    return psw_context.hash(password)

def depend_password(password: str, password_verify: str | None = None) -> HTTPException | None:
    if password_verify:
        if not password == password_verify:
            raise PasswordNotValidCreate
    if not password.isascii():
        raise PasswordNotAscii
    if not search(r'[a-z]', password):
        raise PasswordLowerCase
    if not search(r'[A-Z]', password):
        raise PasswordUpperCase
    if not search(r'[\W_]', password):
        raise PasswordChar
    if not search(r'[0-9]', password):
        raise PasswordNum