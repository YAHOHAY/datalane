from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from playwright.async_api import async_playwright

from config.settings import TARGET_URL
from core.models import JobContext, PipelineData
from core.registry import register_async_ingest

_NAVIGATION_TIMEOUT_MS = 30_000


async def fetch_page_html(url: str) -> str | None:
    try:
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=True)
            try:
                page = await browser.new_page()
                await page.goto(url, wait_until="networkidle", timeout=_NAVIGATION_TIMEOUT_MS)
                html = await page.content()
                return html if html else None
            finally:
                await browser.close()
    except PlaywrightTimeoutError as exc:
        print(f"[playwright] Timeout for {url}: {exc}")
        return None
    except Exception as exc:
        print(f"[playwright] Failed for {url}: {exc}")
        return None


@register_async_ingest("playwright_web")
async def ingest_playwright(params: dict, ctx: JobContext) -> PipelineData:
    url = ctx.params.get("url") or params.get("url") or TARGET_URL
    html = await fetch_page_html(url)
    if html is None:
        raise RuntimeError(f"Failed to fetch page: {url}")
    return PipelineData(payload={"html": html, "url": url})


async def fetch_page_content() -> str | None:
    """Legacy helper used by old scraper shim."""
    return await fetch_page_html(TARGET_URL)
