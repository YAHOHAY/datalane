import re
from typing import TypedDict

from bs4 import BeautifulSoup

from core.models import JobContext, PipelineData
from core.registry import register_transform

SUMMARY_MAX_LENGTH = 500
_IMPORTANT_KEYWORDS_ZH = ("更新", "最新")


class ParseResult(TypedDict):
    summary: str
    is_important: bool


def html_to_plain_text(html_content: str) -> str:
    soup = BeautifulSoup(html_content, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    text = soup.get_text(separator=" ", strip=True)
    return re.sub(r"\s+", " ", text).strip()


def contains_important_keyword(text: str) -> bool:
    if "error" in text.lower():
        return True
    return any(keyword in text for keyword in _IMPORTANT_KEYWORDS_ZH)


def parse_content(html_content: str) -> ParseResult:
    plain_text = html_to_plain_text(html_content)
    return {
        "summary": plain_text[:SUMMARY_MAX_LENGTH],
        "is_important": contains_important_keyword(plain_text),
    }


@register_transform("keyword_alert")
def transform_keyword_alert(data: PipelineData, params: dict, ctx: JobContext) -> PipelineData:
    html = data.get("html")
    if not html:
        raise ValueError("keyword_alert transform requires payload['html']")

    result = parse_content(html)
    data.payload.update(result)
    print(
        f"[transform] summary_len={len(result['summary'])}, "
        f"is_important={result['is_important']}"
    )
    return data
