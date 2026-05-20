"""WhatsApp 推送插件（预留，建议接入 WhatsApp Business Cloud API）。"""

from core.models import JobContext, PipelineData
from core.registry import register_deliver


@register_deliver("whatsapp_text")
def deliver_whatsapp_text(data: PipelineData, params: dict, ctx: JobContext) -> bool:
    raise NotImplementedError(
        "whatsapp_text 尚未实现。请在 config/settings.py 增加 WA 配置后在此对接 API。"
    )
