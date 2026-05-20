# Datalane

**Datalane** — 数据采集 · 清洗 · 推送流水线（仓库目录名可为 `best-ai-monitor`）。

## 目录结构

```text
best-ai-monitor/
├── config/
│   └── settings.py          # Bot、路径、.env
├── core/
│   ├── pipeline.py          # 跑一条 Job
│   ├── triggers.py          # 定时 / CLI
│   ├── job_loader.py
│   ├── models.py
│   └── registry.py
├── plugins/
│   ├── ingest/
│   │   ├── dongqiudi.py
│   │   └── playwright_web.py
│   ├── transform/
│   │   ├── html_to_text.py
│   │   └── pandas_clean.py  # 预留
│   └── deliver/
│       ├── telegram.py
│       └── whatsapp.py      # 预留
├── jobs/
│   ├── dongqiudi_schedule.yaml
│   └── web_monitor.yaml
├── scripts/
│   ├── run_job.py           # ★ 主入口
│   ├── scheduler.py
│   └── test_setup.py
├── legacy/                  # 旧命令兼容
├── data/
└── docs/
```

## 快速开始

```powershell
pip install -r requirements.txt
playwright install
copy .env.example .env

python scripts/run_job.py --list
python scripts/run_job.py dongqiudi_schedule
python scripts/test_setup.py
```

## 任务

| Job ID | 说明 |
|--------|------|
| `dongqiudi_schedule` | 懂球帝赛程 → CSV/TXT → Telegram |
| `web_monitor` | 网页关键词监控 → Telegram |

别名：`dongqiudi` → `dongqiudi_schedule`

## 定时（每天 00:00）

```powershell
setup_windows_task.bat
# 或
python scripts/scheduler.py
```

## 文档

- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — **架构说明、使用指南、扩展 100 任务**
- [docs/FILE_MAP.md](docs/FILE_MAP.md) — 文件对照
