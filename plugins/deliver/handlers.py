from core.models import JobContext, PipelineData
from core.registry import register_deliver
from plugins.deliver.telegram import send_long_text, send_to_telegram


@register_deliver("telegram_long_text")
def deliver_long_text(data: PipelineData, params: dict, ctx: JobContext) -> bool:
    text = data.get("text") or ""
    if not text.strip():
        print("[deliver] Empty text, skip.")
        return False

    header = params.get("header", "")
    if header:
        header = header.format(**data.payload)
    if send_long_text(text, header=header):
        print("[deliver] Schedule sent to Telegram.")
        return True
    print("[deliver] Failed to send schedule.")
    return False


@register_deliver("telegram_alert")
def deliver_alert(data: PipelineData, params: dict, ctx: JobContext) -> bool:
    if not data.get("is_important"):
        print("[deliver] Not important, skip Telegram alert.")
        return True

    summary = data.get("summary") or ""
    prefix = params.get("prefix", "🚨 *监控警报*")
    message = f"{prefix}\n\n{summary}"
    parse_mode = params.get("parse_mode", "Markdown")

    if send_to_telegram(message, parse_mode=parse_mode):
        print("[deliver] Alert sent to Telegram.")
        return True
    print("[deliver] Failed to send alert.")
    return False
