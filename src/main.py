from fastapi import FastAPI

from src.api.user_router import router as user_router

app = FastAPI(title='Сервис авторизации')

app.include_router(user_router)