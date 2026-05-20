"""
Datalane 自检

用法:
  python scripts/test_setup.py
  python scripts/test_setup.py --crawl
"""

import argparse
import sys
from pathlib import Path

from config.settings import (
    CRAWL_END_DATE,
    CRAWL_START_DATE,
    ENV_PATH,
    TARGET_URL,
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
)
from plugins.deliver.telegram import send_to_telegram

_PLACEHOLDER_MARKERS = ("your_", "example.com", "here")


def _is_placeholder(value: str | None) -> bool:
    if not value or not value.strip():
        return True
    lower = value.strip().lower()
    return any(marker in lower for marker in _PLACEHOLDER_MARKERS)


def _validate_bot_token(token: str) -> bool:
    if ":" not in token:
        return False
    bot_id, secret = token.split(":", 1)
    return bot_id.isdigit() and len(secret) > 10


def check_config() -> bool:
    ok = True
    print("=== Datalane 配置检查 ===")
    print(f"  [INFO] .env: {ENV_PATH}")
    for name, value in [
        ("TELEGRAM_BOT_TOKEN", TELEGRAM_BOT_TOKEN),
        ("TELEGRAM_CHAT_ID", TELEGRAM_CHAT_ID),
        ("TARGET_URL", TARGET_URL),
    ]:
        if _is_placeholder(value):
            print(f"  [FAIL] {name}")
            ok = False
        else:
            print(f"  [OK]   {name}")

    if not _is_placeholder(TELEGRAM_BOT_TOKEN) and not _validate_bot_token(TELEGRAM_BOT_TOKEN):
        print("  [FAIL] TELEGRAM_BOT_TOKEN 须为「数字:密钥」完整格式")
        ok = False

    if CRAWL_START_DATE or CRAWL_END_DATE:
        print(f"  [INFO] 赛程: {CRAWL_START_DATE} ~ {CRAWL_END_DATE}")
    return ok


def test_telegram() -> bool:
    print("\n=== Telegram ===")
    if send_to_telegram("Datalane 测试消息"):
        print("  [OK] 已发送")
        return True
    print("  [FAIL]")
    return False


def test_crawl() -> bool:
    print("\n=== 懂球帝抽样 ===")
    import plugins  # noqa: F401
    from datetime import date

    from core.pipeline import run_job

    today = date.today().isoformat()
    try:
        run_job("dongqiudi", deliver=False, start=today, end=today)
        return True
    except Exception as exc:
        print(f"  [FAIL] {exc}")
        return False


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--crawl", action="store_true")
    args = parser.parse_args()

    if not check_config():
        sys.exit(1)
    if not test_telegram():
        sys.exit(1)
    if args.crawl and not test_crawl():
        sys.exit(1)
    print("\n通过。赛程: python run_job.py dongqiudi")


if __name__ == "__main__":
    main()
