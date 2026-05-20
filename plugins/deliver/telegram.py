import requests

from config.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from core.models import JobContext, PipelineData
from core.registry import register_deliver

_TELEGRAM_API_URL = "https://api.telegram.org/bot{token}/sendMessage"
_REQUEST_TIMEOUT_SEC = 30
_TELEGRAM_MAX_LENGTH = 4000


def send_to_telegram(message: str, parse_mode: str | None = None) -> bool:
    url = _TELEGRAM_API_URL.format(token=TELEGRAM_BOT_TOKEN)
    payload: dict = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    if parse_mode:
        payload["parse_mode"] = parse_mode

    try:
        response = requests.post(url, json=payload, timeout=_REQUEST_TIMEOUT_SEC)
        response.raise_for_status()
        body = response.json()
        if not body.get("ok"):
            print(f"[telegram] API error: {body}")
            return False
        return True
    except requests.RequestException as exc:
        print(f"[telegram] Send failed: {exc}")
        return False


def _split_text(text: str, max_len: int) -> list[str]:
    if len(text) <= max_len:
        return [text]

    parts: list[str] = []
    start = 0
    while start < len(text):
        end = start + max_len
        if end < len(text):
            split_at = text.rfind("\n", start, end)
            if split_at <= start:
                split_at = end
            else:
                end = split_at + 1
        parts.append(text[start:end].strip())
        start = end
    return [part for part in parts if part]


def send_long_text(text: str, header: str = "") -> bool:
    body = f"{header}\n\n{text}".strip() if header else text.strip()
    if not body:
        print("[telegram] Nothing to send.")
        return False

    parts = _split_text(body, _TELEGRAM_MAX_LENGTH)
    all_ok = True
    for index, part in enumerate(parts, start=1):
        chunk = f"({index}/{len(parts)})\n{part}" if len(parts) > 1 else part
        if not send_to_telegram(chunk):
            all_ok = False
    return all_ok


@register_deliver("telegram_long_text")
def deliver_long_text(data: PipelineData, params: dict, ctx: JobContext) -> bool:
    text = data.get("text") or ""
    if not text.strip():
        print("[telegram] Empty text, skip.")
        return False

    header = params.get("header", "")
    if header:
        header = header.format(**data.payload)
    if send_long_text(text, header=header):
        print("[telegram] Schedule sent.")
        return True
    return False


@register_deliver("telegram_alert")
def deliver_alert(data: PipelineData, params: dict, ctx: JobContext) -> bool:
    if not data.get("is_important"):
        print("[telegram] Not important, skip alert.")
        return True

    summary = data.get("summary") or ""
    prefix = params.get("prefix", "🚨 *监控警报*")
    message = f"{prefix}\n\n{summary}"
    parse_mode = params.get("parse_mode", "Markdown")

    if send_to_telegram(message, parse_mode=parse_mode):
        print("[telegram] Alert sent.")
        return True
    return False
