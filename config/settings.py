import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field

ROOT_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT_DIR / ".env"
JOBS_DIR = ROOT_DIR / "jobs"
DATA_DIR = ROOT_DIR / "data"

load_dotenv(ENV_PATH)


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


class Settings(BaseModel):
    telegram_bot_token: str = Field(..., description="Telegram bot token")
    telegram_chat_id: str = Field(..., description="Telegram chat ID")
    target_url: str = Field(..., description="URL to monitor")


settings = Settings(
    telegram_bot_token=_require_env("TELEGRAM_BOT_TOKEN"),
    telegram_chat_id=_require_env("TELEGRAM_CHAT_ID"),
    target_url=_require_env("TARGET_URL"),
)

TELEGRAM_BOT_TOKEN = settings.telegram_bot_token
TELEGRAM_CHAT_ID = settings.telegram_chat_id
TARGET_URL = settings.target_url

CRAWL_START_DATE = os.getenv("CRAWL_START_DATE")
CRAWL_END_DATE = os.getenv("CRAWL_END_DATE")
