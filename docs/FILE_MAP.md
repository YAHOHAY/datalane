# 文件对照表（重构后）

根目录旧脚本已改为**薄入口**，逻辑在 `plugins/` / `core/` / `jobs/`。

| 你熟悉的文件 | 现在在哪 | 怎么运行 |
|-------------|----------|----------|
| `dongqiudi_crawler.py` | `plugins/ingest/dongqiudi.py` | `python run_job.py dongqiudi` |
| `notifier.py` | `plugins/deliver/telegram.py` | 由 Job 的 deliver 步骤调用 |
| `parser.py` | `plugins/transform/html_clean.py` | `web_monitor` 任务自动用 |
| `scraper.py` | `plugins/ingest/playwright_web.py` | `python run_job.py web_monitor` |
| `config.py` | `config/settings.py` | `from config import TELEGRAM_BOT_TOKEN` |
| `fetch_matches.py` | 根目录入口 + `jobs/dongqiudi.yaml` | `python fetch_matches.py --telegram` |
| `daily_job.py` | 根目录入口 | `python daily_job.py` |
| `main.py` | 根目录入口 | `python main.py` |
| `test_setup.py` | 根目录 + `scripts/test_setup.py` | `python test_setup.py` |
| `scheduler.py` | 根目录 + `scripts/scheduler.py` | `python scheduler.py` |

## 不会出现在 GitHub 上的（正常）

| 文件/目录 | 原因 |
|-----------|------|
| `.env` | 含密钥，在 `.gitignore` |
| `data/*.csv` `data/*.txt` | 运行输出，在 `.gitignore` |
| `.venv/` | 本地虚拟环境 |

克隆仓库后请：`copy .env.example .env` 并填写配置。
