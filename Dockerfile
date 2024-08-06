FROM python:3.12.4-alpine3.20
COPY . /src

WORKDIR /src

EXPOSE 8000

RUN python -m pip install pip --upgrade && python -m pip install --no-cache-dir --upgrade poetry && python -m poetry install

CMD ["python", "-m", "poetry", "run", "alembic", "upgrade", "head", "&&", "python", "-m", "poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "4000", "--reload"]