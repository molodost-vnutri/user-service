from fastapi import FastAPI

from src.router import router

app = FastAPI(title='Сервис авторизации')

app.include_router(router)