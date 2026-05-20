import csv
import random
import time
from datetime import date, datetime, timedelta
from pathlib import Path

import requests

from config.settings import CRAWL_END_DATE, CRAWL_START_DATE, DATA_DIR
from core.models import JobContext, PipelineData
from core.registry import register_ingest

DEFAULT_RANGE_DAYS = 7
_WEEKDAYS_ZH = ("星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日")

_API_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    ),
    "Referer": "https://www.dongqiudi.com/live/10",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Origin": "https://www.dongqiudi.com",
}
_API_URL = "https://www.dongqiudi.com/api/data/tab/new/important"


def default_date_range() -> tuple[str, str]:
    start = date.today()
    end = start + timedelta(days=DEFAULT_RANGE_DAYS - 1)
    return start.isoformat(), end.isoformat()


def resolve_date_range(
    start: str | None = None,
    end: str | None = None,
) -> tuple[str, str]:
    if start or end:
        if not (start and end):
            raise ValueError("Both start and end dates are required.")
        _validate_date_str(start)
        _validate_date_str(end)
        if datetime.strptime(start, "%Y-%m-%d") > datetime.strptime(end, "%Y-%m-%d"):
            raise ValueError(f"Start date {start} must not be after end date {end}.")
        return start, end

    if CRAWL_START_DATE or CRAWL_END_DATE:
        if not (CRAWL_START_DATE and CRAWL_END_DATE):
            raise ValueError("Set both CRAWL_START_DATE and CRAWL_END_DATE in .env, or leave both empty.")
        _validate_date_str(CRAWL_START_DATE)
        _validate_date_str(CRAWL_END_DATE)
        return CRAWL_START_DATE, CRAWL_END_DATE

    return default_date_range()


def _validate_date_str(value: str) -> None:
    datetime.strptime(value, "%Y-%m-%d")


def fetch_matches_to_files(
    start_date_str: str,
    end_date_str: str,
    output_dir: Path | None = None,
) -> tuple[Path, Path, str]:
    out_dir = output_dir or DATA_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    current_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    session = requests.Session()
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = out_dir / f"matches_{stamp}.csv"
    txt_path = out_dir / f"matches_{stamp}.txt"

    with (
        open(csv_path, mode="w", newline="", encoding="utf-8-sig") as csv_file,
        open(txt_path, mode="w", encoding="utf-8") as txt_file,
    ):
        writer = csv.writer(csv_file)
        writer.writerow(["比赛日期", "星期", "开赛时间", "赛事名称", "主队", "VS", "客队"])
        print(f"[dongqiudi] TXT: {txt_path}\n[dongqiudi] CSV: {csv_path}\n")

        is_first_day = True
        while current_date <= end_date:
            date_query = current_date.strftime("%Y-%m-%d")
            api_time = f"{date_query}%2000:00:00next"
            url = f"{_API_URL}?start={api_time}&init=1&platform=www"

            try:
                time.sleep(random.uniform(1.5, 3.0))
                response = session.get(url, headers=_API_HEADERS, timeout=10)
                response.raise_for_status()

                matches = response.json().get("list", [])
                weekday = _WEEKDAYS_ZH[current_date.weekday()]
                date_header = f"{date_query} {weekday}"
                print(f"\n{date_header}")

                if not is_first_day:
                    txt_file.write("\n")
                txt_file.write(f"{date_header}\n")
                is_first_day = False

                for match in matches:
                    if match.get("relate_type") == "match" and match.get("date_utc") == date_query:
                        match_time = match.get("start_play", "")[11:16]
                        comp_name = match.get("competition_name", "")
                        team_a = match.get("team_A_name", "")
                        team_b = match.get("team_B_name", "")
                        txt_line = f"{match_time} {comp_name:<8} {team_a}   VS   {team_b}"
                        print(txt_line)
                        txt_file.write(f"{txt_line}\n")
                        writer.writerow([date_query, weekday, match_time, comp_name, team_a, "VS", team_b])
            except requests.RequestException as exc:
                print(f"[dongqiudi] {date_query} failed: {exc}")
                time.sleep(5)

            current_date += timedelta(days=1)

    text = txt_path.read_text(encoding="utf-8").strip()
    print(f"\n[dongqiudi] Done: {csv_path.name}, {txt_path.name}")
    return csv_path, txt_path, text


@register_ingest("dongqiudi")
def ingest_dongqiudi(params: dict, ctx: JobContext) -> PipelineData:
    start = ctx.params.get("start")
    end = ctx.params.get("end")
    start, end = resolve_date_range(start, end)

    csv_path, txt_path, text = fetch_matches_to_files(start, end)
    return PipelineData(
        payload={
            "start": start,
            "end": end,
            "text": text,
            "csv_path": str(csv_path),
            "txt_path": str(txt_path),
        }
    )

