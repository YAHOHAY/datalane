# Legacy 兼容入口

这些脚本仅转发到 `scripts/run_job.py` 与新架构，**不要再在此写业务逻辑**。

| 文件 | 请改用 |
|------|--------|
| `legacy/fetch_matches.py` | `python scripts/run_job.py dongqiudi_schedule --telegram` |
| `legacy/daily_job.py` | `python scripts/run_job.py dongqiudi_schedule` |
| `legacy/main.py` | `python scripts/run_job.py web_monitor` |
