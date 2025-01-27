import json
import os
from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    CLIENT_ID: str = os.getenv("CLIENT_ID")
    CLIENT_SECRET: str = os.getenv("CLIENT_SECRET")
    WEBHOOK_URL: str = os.getenv("WEBHOOK_URL")
    AVITO_USER_ID: int = os.getenv("AVITO_USER_ID")

    ADMIN_TG_ID: int = os.getenv("ADMIN_TG_ID")

    DB_HOST: str = os.environ.get("DB_HOST")
    DB_PORT: str = os.environ.get("DB_PORT")
    DB_NAME: str = os.environ.get("DB_NAME")
    DB_USER: str = os.environ.get("DB_USER")
    DB_PASS: str = os.environ.get("DB_PASS")
    db_url: str = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    BOT_TOKEN = os.environ.get("BOT_TOKEN")

    DEPARTMENTS_GROUPS_IDS: dict = json.loads(os.environ.get("DEPARTMENTS_GROUPS_IDS", {}))
    DEPARTMENTS_CLIENT_SECRETS: list[dict[str, str]] = json.loads(os.environ.get("DEPARTMENTS_CLIENT_SECRETS"))


settings = Settings()
