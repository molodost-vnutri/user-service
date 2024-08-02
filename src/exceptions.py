from fastapi import HTTPException

IncorrectJwtToken = HTTPException(
    status_code=401,
    detail='Токен не валидный'
)

ExpireJwtToken = HTTPException(
    status_code=401,
    detail='Токен истёк'
)

TokenNotFound = HTTPException(
    status_code=401,
    detail='Токен не найден'
)

PasswordNotValidCreate = HTTPException(
    status_code=409,
    detail='Пароли не совпадают'
)

PasswordLowerCase = HTTPException(
    status_code=409,
    detail='Пароль должен содержать минимум один символ нижнего регистра'
)

PasswordUpperCase = HTTPException(
    status_code=409,
    detail='Пароль должен содержать минимум один символ верхнего регистра'
)

PasswordNum = HTTPException(
    status_code=409,
    detail='Пароль должен содержать минимум одно число'
)

PasswordChar = HTTPException(
    status_code=409,
    detail='Пароль должен содержать минимум один спец символ'
)

PasswordNotAscii = HTTPException(
    status_code=409,
    detail='Пароль должен быть только из печатаемых символов'
)

PasswordIncorrect = HTTPException(
    status_code=409,
    detail='Неверный пароль'
)

MailOrPasswordIncorrect = HTTPException(
    status_code=401,
    detail='Почта или пароль невалидны'
)